import requests
import datetime

WEATHER_API_KEY = "9ebb0e8593cbacd011c49a49138c6392"

def get_live_weather(city="Karachi"):
    try:
        url = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={WEATHER_API_KEY}&units=imperial"
        )
        data     = requests.get(url, timeout=5).json()
        temp     = data['main']['temp']
        humidity = data['main']['humidity']
        rain     = data.get('rain', {}).get('1h', 0.0)
        clouds   = data['clouds']['all'] / 100.0

        return {
            "temp"            : round(temp, 1),
            "humidity"        : round(humidity, 1),
            "rain"            : round(min(rain, 1.0), 3),
            "weather_severity": round(clouds * 0.4 + min(rain,1) * 0.6, 3),
            "success"         : True
        }
    except Exception as e:
        return {
            "temp"            : 65.0,
            "humidity"        : 60.0,
            "rain"            : 0.0,
            "weather_severity": 0.1,
            "success"         : False
        }

def get_live_time():
    now          = datetime.datetime.now()
    hour         = now.hour
    day_of_week  = now.weekday()
    is_weekend   = 1 if day_of_week >= 5 else 0
    is_peak_hour = 1 if (7 <= hour <= 9 or 17 <= hour <= 20) else 0
    return {
        "hour"        : hour,
        "day_of_week" : day_of_week,
        "is_weekend"  : is_weekend,
        "is_peak_hour": is_peak_hour
    }

def get_live_demand(hour):
    if 7 <= hour <= 9:
        return {"demand_index": 0.85, "route_demand": 2000}
    elif 17 <= hour <= 20:
        return {"demand_index": 0.90, "route_demand": 2500}
    elif 0 <= hour <= 5:
        return {"demand_index": 0.40, "route_demand": 500}
    else:
        return {"demand_index": 0.55, "route_demand": 1000}

def get_all_live_data(city="Karachi", distance=3.5):
    weather = get_live_weather(city)
    time    = get_live_time()
    demand  = get_live_demand(time['hour'])
    return {
        "distance"        : distance,
        "hour"            : time['hour'],
        "day_of_week"     : time['day_of_week'],
        "is_weekend"      : time['is_weekend'],
        "is_peak_hour"    : time['is_peak_hour'],
        "demand_index"    : demand['demand_index'],
        "route_demand"    : demand['route_demand'],
        "temp"            : weather['temp'],
        "rain"            : weather['rain'],
        "humidity"        : weather['humidity'],
        "weather_severity": weather['weather_severity'],
        "weather_success" : weather['success']
    }