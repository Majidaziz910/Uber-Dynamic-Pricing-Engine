# Uber-Dynamic-Pricing-Engine

# Uber Dynamic Pricing Engine

A complete end-to-end machine learning system that predicts and adjusts ride prices in real-time using XGBoost + Reinforcement Learning (PPO).

## Live Demo
- FastAPI Server: `http://127.0.0.1:8000/docs`
- Streamlit Dashboard: `http://localhost:8501`

## Results
| Metric | Value |
|--------|-------|
| MAE Score | 0.0232 |
| RMSE Score | 0.0829 |
| Revenue Lift | +25% vs static |
| API Latency | <50ms |
| RL Training | 100K steps |

## Project Structure
```
pricing_project/
├── main.py              # FastAPI server
├── dashboard.py         # Streamlit dashboard
├── auto_data.py         # Live weather data
├── requirements.txt     # Dependencies
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## Setup Instructions

### Step 1 — Clone the repo
```bash
git clone https://github.com/yourusername/uber-dynamic-pricing.git
cd uber-dynamic-pricing
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Add your trained models
Download from Google Drive and place in project folder:
- `xgb_model.pkl`
- `rl_pricing_agent.zip`

### Step 4 — Run FastAPI server
```bash
uvicorn main:app --reload
```

### Step 5 — Run Streamlit dashboard
```bash
streamlit run dashboard.py
```

## Tech Stack
- **ML Model:** XGBoost
- **RL Agent:** Stable-Baselines3 (PPO)
- **RL Environment:** Gymnasium
- **API:** FastAPI + Uvicorn
- **Dashboard:** Streamlit + Plotly
- **Data:** Pandas, NumPy
- **Weather:** OpenWeatherMap API

## Pipeline
```
Raw Data (86MB)
     ↓
EDA + Feature Engineering
     ↓
XGBoost Model (MAE: 0.023)
     ↓
PPO RL Agent (100K steps)
     ↓
Simulation + Evaluation
     ↓
FastAPI Server
     ↓
Streamlit Dashboard
```

## Dataset
- Uber/Lyft cab rides dataset — Boston, MA
- 86MB rides data + weather data
- Source: Kaggle — Uber and Lyft Dataset Boston MA

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Server status |
| `/health` | GET | Model health check |
| `/surge-status` | GET | Current surge level |
| `/predict-price` | POST | Price prediction |

## Sample API Request
```json
{
  "distance": 3.5,
  "hour": 8,
  "day_of_week": 0,
  "is_weekend": 0,
  "is_peak_hour": 1,
  "demand_index": 0.85,
  "temp": 55.0,
  "rain": 0.3,
  "humidity": 70.0,
  "weather_severity": 0.5,
  "route_demand": 1200
}
```

## Sample API Response
```json
{
  "base_price": 10.0,
  "xgb_multiplier": 0.998,
  "rl_multiplier": 2.75,
  "final_multiplier": 2.75,
  "final_price": 27.5,
  "recommended_by": "RL Agent",
  "status": "High Surge"
}
```

## Author
Built as a complete portfolio project demonstrating end-to-end ML engineering skills.

## License
MIT License
