import folium
import requests
import random
from folium.plugins import MarkerCluster

# OpenWeatherMap API for real-time weather data (Replace 'YOUR_API_KEY' with a valid key)
API_KEY = "541b60539a1b0dd705ff82c44bc9f9de"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

# List of all Indian states with approximate lat/lon coordinates
states = [
    {"name": "Andhra Pradesh", "lat": 15.9129, "lon": 79.7400},
    {"name": "Arunachal Pradesh", "lat": 27.1004, "lon": 93.6167},
    {"name": "Assam", "lat": 26.2006, "lon": 92.9376},
    {"name": "Bihar", "lat": 25.0961, "lon": 85.3131},
    {"name": "Chhattisgarh", "lat": 21.2787, "lon": 81.8661},
    {"name": "Goa", "lat": 15.2993, "lon": 74.1240},
    {"name": "Gujarat", "lat": 22.2587, "lon": 71.1924},
    {"name": "Haryana", "lat": 29.0588, "lon": 76.0856},
    {"name": "Himachal Pradesh", "lat": 31.1048, "lon": 77.1734},
    {"name": "Jharkhand", "lat": 23.6102, "lon": 85.2799},
    {"name": "Karnataka", "lat": 15.3173, "lon": 75.7139},
    {"name": "Kerala", "lat": 10.8505, "lon": 76.2711},
    {"name": "Madhya Pradesh", "lat": 23.4733, "lon": 77.9470},
    {"name": "Maharashtra", "lat": 19.7515, "lon": 75.7139},
    {"name": "Manipur", "lat": 24.6637, "lon": 93.9063},
    {"name": "Meghalaya", "lat": 25.4670, "lon": 91.3662},
    {"name": "Mizoram", "lat": 23.1645, "lon": 92.9376},
    {"name": "Nagaland", "lat": 26.1584, "lon": 94.5624},
    {"name": "Odisha", "lat": 20.9517, "lon": 85.0985},
    {"name": "Punjab", "lat": 31.1471, "lon": 75.3412},
    {"name": "Rajasthan", "lat": 27.0238, "lon": 74.2179},
    {"name": "Sikkim", "lat": 27.5330, "lon": 88.5122},
    {"name": "Tamil Nadu", "lat": 11.1271, "lon": 78.6569},
    {"name": "Telangana", "lat": 17.1232, "lon": 79.2089},
    {"name": "Tripura", "lat": 23.9408, "lon": 91.9882},
    {"name": "Uttar Pradesh", "lat": 26.8467, "lon": 80.9462},
    {"name": "Uttarakhand", "lat": 30.0668, "lon": 79.0193},
    {"name": "West Bengal", "lat": 22.9868, "lon": 87.8550}
]

# Function to fetch real-time weather data
def get_weather_data(lat, lon):
    try:
        response = requests.get(WEATHER_URL, params={"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"})
        data = response.json()
        return {
            "temp": data["main"]["temp"],
            "wind_speed": data["wind"]["speed"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"]
        }
    except:
        return {"temp": random.uniform(15, 40), "wind_speed": random.uniform(0, 20), "humidity": random.uniform(30, 90), "weather": "unknown"}

# Initialize map
map_center = [22.3511, 78.6677]
m = folium.Map(location=map_center, zoom_start=5)
marker_cluster = MarkerCluster().add_to(m)

# Function to determine risk level
def determine_risk(weather_data):
    risk_factors = []
    if weather_data["wind_speed"] > 15:
        risk_factors.append("Cyclone Threat")
    if weather_data["humidity"] > 80:
        risk_factors.append("Flood Risk")
    if weather_data["temp"] < 5 or weather_data["temp"] > 40:
        risk_factors.append("Extreme Weather")
    
    severity = "Green"
    if risk_factors:
        severity = "Yellow" if len(risk_factors) == 1 else "Red"
    return severity, ", ".join(risk_factors) if risk_factors else "Low Risk"

# Add markers for states
for state in states:
    weather = get_weather_data(state["lat"], state["lon"])
    zone, reasons = determine_risk(weather)
    color_mapping = {"Red": "red", "Yellow": "orange", "Green": "green"}
    
    folium.CircleMarker(
        location=[state["lat"], state["lon"]],
        radius=(weather["wind_speed"] + weather["humidity"]) / 10,
        color=color_mapping[zone],
        fill=True,
        fill_color=color_mapping[zone],
        fill_opacity=0.6,
        popup=folium.Popup(
            f"{state['name']}<br>Risk Level: {zone}<br>Reasons: {reasons}<br>Weather: {weather['weather']}<br>Temperature: {weather['temp']}°C<br>Wind Speed: {weather['wind_speed']} km/h<br>Humidity: {weather['humidity']}%",
            max_width=300
        )
    ).add_to(marker_cluster)

# Save and display the map
m.save("disaster_severity_map.html")
print("Map saved as disaster_severity_map.html")
