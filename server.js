require('dotenv').config();
const express = require('express');
const nodemailer = require('nodemailer');
const cors = require('cors');
const axios = require('axios'); // For fetching weather data

const app = express();
const port = 5000;

app.use(express.json());
app.use(cors());

// Weather API Key (from OpenWeatherMap)
const WEATHER_API_KEY = process.env.WEATHER_API_KEY;

// Nodemailer Configuration for Sending Emails
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS,
    },
});

// ✅ Emergency Contacts + Weather Alerts
app.get('/api/emergency-contacts', async (req, res) => {
    const userLocation = req.query.city || "New York"; // Default city if not provided

    try {
        // Fetch current weather data
        const weatherResponse = await axios.get(`https://api.openweathermap.org/data/2.5/weather?q=${userLocation}&appid=${WEATHER_API_KEY}&units=metric`);
        const weatherData = weatherResponse.data;
        
        // Extract weather details
        const weatherCondition = weatherData.weather[0].main;  // e.g., Rain, Storm, Clear
        const temperature = weatherData.main.temp;
        const city = weatherData.name;

        // Emergency contacts
        const contacts = [
            { name: "City Shelter", type: "Shelter", phone: "7411254552" },
            { name: "General Hospital", type: "Hospital", phone: "7411254552" },
            { name: "Rescue Team 24/7", type: "Rescue", phone: "9353519844" }
        ];

        // Check for dangerous weather conditions
        if (weatherCondition === "Rain" || weatherCondition === "Storm" || weatherCondition === "Extreme") {
            const alertMessage = `🚨 WEATHER ALERT: ${weatherCondition} detected in ${city}. Temperature: ${temperature}°C. Stay safe!`;
            
            // Send Alert Email
            const mailOptions = {
                from: process.env.EMAIL_USER,
                to: "harshithaan2004@gmail.com@example.com", // Change this to the actual user's email
                subject: "🚨 Severe Weather Alert!",
                text: alertMessage,
            };

            transporter.sendMail(mailOptions, (error, info) => {
                if (error) {
                    console.error("Error sending email:", error);
                } else {
                    console.log("Weather alert email sent: " + info.response);
                }
            });
        }

        // Send emergency contacts + weather response
        res.status(200).json({ city, temperature, weatherCondition, contacts });

    } catch (error) {
        console.error("Error fetching weather data:", error);
        res.status(500).json({ success: false, message: "Failed to fetch weather data" });
    }
});

// Start Server
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
