from flask import Flask, request, jsonify
import pickle
import numpy as np
import requests

app = Flask(__name__)

# Load trained model and scaler
with open('C:/Users/harsh/OneDrive/Desktop/flood_prediction/random_forest_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('C:/Users/harsh/OneDrive/Desktop/flood_prediction/scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

# Function to classify earthquake risk based on magnitude
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

# API endpoint for prediction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']
    depth = data['depth']
    
    # Scale and predict
    input_features = np.array([[latitude, longitude, depth]])
    input_features_scaled = scaler.transform(input_features)
    predicted_magnitude = model.predict(input_features_scaled)[0]
    
    # Classify risk
    risk_level = classify_earthquake(predicted_magnitude)
    
    return jsonify({
        'predicted_magnitude': predicted_magnitude,
        'risk_level': risk_level
    })

if __name__ == '__main__':
    app.run(debug=True)
