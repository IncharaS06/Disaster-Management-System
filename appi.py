import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")  # Set template folder for HTML
CORS(app)  # Enable CORS for frontend communication

API_KEY = "e3a90990b56034cdb755847b6439abae"

def classify_earthquake(magnitude):
    if magnitude < 4.5:
        return "Minor (No risk)"
    elif 4.5 <= magnitude < 5.0:
        return "Light (Low risk)"
    elif 5.0 <= magnitude < 7.0:
        return "Moderate (Medium risk)"
    elif 7.0 <= magnitude < 8.0:
        return "Strong (High risk)"
    else:
        return "Severe (Very high risk)"

def classify_flood_risk(rainfall):
    if rainfall == 0:
        return "No risk"
    elif 0 < rainfall <= 20:
        return "Low risk"
    elif 20 < rainfall <= 50:
        return "Medium risk"
    elif 50 < rainfall <= 100:
        return "High risk"
    else:
        return "Severe (Very high risk)"

def classify_cyclone(wind_speed):
    category_mapping = {
        (0, 33): ("Tropical Depression", "Normal"),
        (34, 63): ("Tropical Storm", "Medium intensity"),
        (64, 82): ("Category 1 Hurricane", "Medium intensity"),
        (83, 95): ("Category 2 Hurricane", "High intensity"),
        (96, 112): ("Category 3 Hurricane", "High intensity"),
        (113, 136): ("Category 4 Hurricane", "High intensity"),
        (137, float('inf')): ("Category 5 Hurricane", "Extreme danger")
    }
    for (low, high), (category, intensity) in category_mapping.items():
        if low <= wind_speed <= high:
            return category, intensity
    return "No Cyclone", "No risk"

def get_location_data(place):
    geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={place}&limit=1&appid={API_KEY}"
    response = requests.get(geo_url).json()
    if not response:
        return None, None, None
    location = response[0]
    return place, location['lat'], location['lon']

def get_earthquake_data(lat, lon):
    eq_url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&latitude={lat}&longitude={lon}&maxradius=100&limit=1"
    response = requests.get(eq_url).json()
    if response['features']:
        eq = response['features'][0]['properties']
        return eq['mag'], eq.get('depth', 10)  
    return None, 10

def get_weather_data(lat, lon):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(weather_url).json()
    return {
        'wind_speed': response['wind']['speed'],
        'pressure': response['main']['pressure'],
        'rainfall': response.get('rain', {}).get('1h', 0)  
    }

@app.route("/")
def home():
    return render_template("indexi.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    place_name, lat, lon = get_location_data(data["location"])
    
    if lat is None:
        return jsonify({"error": "Location not found"}), 400

    eq_magnitude, depth = get_earthquake_data(lat, lon)
    weather = get_weather_data(lat, lon)

    eq_risk_level = classify_earthquake(eq_magnitude if eq_magnitude else 0)
    flood_risk_level = classify_flood_risk(weather['rainfall'])
    cyclone_category, cyclone_risk_level = classify_cyclone(weather['wind_speed'])

    response_data = {
        "Place": place_name,
        "Latitude": lat,
        "Longitude": lon,
        "Earthquake Magnitude": round(eq_magnitude, 2) if eq_magnitude else "No recent data",
        "Earthquake Risk": eq_risk_level,
        "Wind Speed (m/s)": weather['wind_speed'],
        "Pressure (hPa)": weather['pressure'],
        "Rainfall (mm)": weather['rainfall'],
        "Flood Risk": flood_risk_level,
        "Cyclone Category": cyclone_category,
        "Cyclone Risk": cyclone_risk_level
    }

    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
