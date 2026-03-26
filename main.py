from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
import uvicorn
import os

app = FastAPI(title="Dynamic Pricing Engine")

# Load XGBoost model
with open("xgb_model.pkl", "rb") as f:
    xgb_model = pickle.load(f)
print("XGBoost loaded!")

# Load RL model safely
if os.path.exists("rl_pricing_agent.zip"):
    from stable_baselines3 import PPO
    rl_model = PPO.load("rl_pricing_agent")
    print("RL Agent loaded!")
else:
    rl_model = None
    print("RL Agent not found — XGBoost only mode")

class RideRequest(BaseModel):
    distance         : float
    hour             : int
    day_of_week      : int
    is_weekend       : int
    is_peak_hour     : int
    demand_index     : float
    temp             : float
    rain             : float
    humidity         : float
    weather_severity : float
    route_demand     : int

@app.get("/")
def home():
    return {
        "message"   : "Dynamic Pricing Engine is running!",
        "xgb_model" : "loaded",
        "rl_agent"  : "loaded" if rl_model else "not loaded"
    }

@app.get("/health")
def health():
    return {
        "status"    : "healthy",
        "xgb_model" : "loaded",
        "rl_agent"  : "loaded" if rl_model else "not loaded"
    }

@app.get("/surge-status")
def surge_status():
    import datetime
    hour    = datetime.datetime.now().hour
    is_peak = 1 if (7 <= hour <= 9 or 17 <= hour <= 20) else 0
    return {
        "current_hour" : hour,
        "is_peak"      : is_peak,
        "surge"        : 1.8 if is_peak else 1.0,
        "message"      : "Peak hours" if is_peak else "Normal hours"
    }

@app.post("/predict-price")
def predict_price(ride: RideRequest):
    try:
        base_price = 10.0

        # XGBoost — 6 features only (same as Step 3 training)
        xgb_input = np.array([[
            ride.distance,
            ride.hour,
            ride.day_of_week,
            ride.is_weekend,
            ride.is_peak_hour,
            ride.demand_index
        ]])

        xgb_multiplier = float(np.clip(xgb_model.predict(xgb_input)[0], 0.5, 3.0))

        # RL Agent — 5 features (same as Step 4 training)
        if rl_model is not None:
            state = np.array([
                ride.hour / 23.0,
                float(ride.is_peak_hour),
                ride.demand_index,
                min(ride.rain, 1.0),
                ride.weather_severity
            ], dtype=np.float32)

            action, _     = rl_model.predict(state, deterministic=True)
            rl_multiplier = float(0.5 + (int(action) * 0.25))
        else:
            rl_multiplier = xgb_multiplier

        # Pick final multiplier
        if ride.is_peak_hour == 1:
            final_multiplier = max(xgb_multiplier, rl_multiplier)
            recommended_by   = "XGBoost" if xgb_multiplier >= rl_multiplier else "RL Agent"
        else:
            final_multiplier = min(xgb_multiplier, rl_multiplier)
            recommended_by   = "XGBoost" if xgb_multiplier <= rl_multiplier else "RL Agent"

        final_price = round(base_price * final_multiplier, 2)

        if final_multiplier >= 2.0:
            status = "High Surge"
        elif final_multiplier >= 1.25:
            status = "Moderate Surge"
        else:
            status = "Normal"

        return {
            "base_price"       : base_price,
            "xgb_multiplier"   : round(xgb_multiplier, 3),
            "rl_multiplier"    : round(rl_multiplier, 3),
            "final_multiplier" : round(final_multiplier, 3),
            "final_price"      : final_price,
            "recommended_by"   : recommended_by,
            "status"           : status
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)