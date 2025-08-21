import pickle
import os
import random
from datetime import datetime, timedelta
import holidays
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests
import json


class TrafficPredictor:
    def __init__(self):
        self.model = None
        self.geolocator = Nominatim(user_agent="traffic_predictor")
        self.india_holidays = holidays.India()
        self.load_model()
    
    def load_model(self):
        """Load the trained model from pickle file"""
        model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'traffic_model.pkl')
        
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print("Model loaded successfully")
            except Exception as e:
                print(f"Error loading model: {e}")
                self.model = None
        else:
            print("Model file not found, using fallback prediction")
            self.model = None
    
    def get_coordinates(self, location):
        """Get coordinates for a location using Nominatim API"""
        try:
            location_data = self.geolocator.geocode(f"{location}, India")
            if location_data:
                return location_data.latitude, location_data.longitude
        except Exception as e:
            print(f"Error getting coordinates: {e}")
        
        # Fallback coordinates for major cities
        city_coords = {
            'Delhi': (28.7041, 77.1025),
            'Mumbai': (19.0760, 72.8777),
            'Bengaluru': (12.9716, 77.5946),
            'Hyderabad': (17.3850, 78.4867),
            'Chennai': (13.0827, 80.2707),
            'Kolkata': (22.5726, 88.3639),
        }
        
        for city, coords in city_coords.items():
            if city.lower() in location.lower():
                return coords
        
        # Random coordinates in India as last resort
        return (random.uniform(8, 37), random.uniform(68, 97))
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points using Haversine formula"""
        return geodesic((lat1, lon1), (lat2, lon2)).kilometers
    
    def get_weather_data(self, city):
        """Get weather data from OpenWeather API or generate synthetic data"""
        try:
            # You can add your OpenWeather API key here
            api_key = "your_openweather_api_key"  # Replace with actual key
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return data['weather'][0]['main']
        except Exception as e:
            print(f"Weather API error: {e}")
        
        # Fallback: synthetic weather based on time and season
        weather_conditions = ['Clear', 'Clouds', 'Rain', 'Thunderstorm']
        weights = [0.4, 0.3, 0.2, 0.1]
        return random.choices(weather_conditions, weights=weights)[0]
    
    def get_route_type(self, distance):
        """Determine route type based on distance"""
        if distance < 5:
            return 'local'
        elif distance < 15:
            return 'suburban'
        else:
            return 'highway'
    
    def get_event_flag(self, hour, weekday):
        """Simulate event flag based on time and day"""
        # Higher probability during peak hours and weekends
        if weekday in [5, 6]:  # Weekend
            base_prob = 0.3
        else:
            base_prob = 0.1
        
        if 8 <= hour <= 10 or 17 <= hour <= 19:  # Peak hours
            base_prob += 0.2
        
        return random.random() < base_prob
    
    def predict_congestion(self, features):
        """Make prediction using the loaded model or fallback logic"""
        if self.model:
            try:
                # Ensure features match the expected format
                feature_names = ["city", "distance_km", "hour", "weekday", "day_type", "weather", "event", "route_type"]
                feature_values = [
                    features['city'],
                    features['distance_km'],
                    features['hour'],
                    features['weekday'],
                    features['day_type'],
                    features['weather'],
                    features['event'],
                    features['route_type']
                ]
                
                # Make prediction
                prediction = self.model.predict([feature_values])[0]
                probabilities = self.model.predict_proba([feature_values])[0]
                
                return prediction, probabilities
            except Exception as e:
                print(f"Model prediction error: {e}")
        
        # Fallback prediction logic
        return self._fallback_prediction(features)
    
    def _fallback_prediction(self, features):
        """Fallback prediction logic when model is not available"""
        distance = features['distance_km']
        hour = features['hour']
        weekday = features['weekday']
        weather = features['weather']
        event = features['event']
        
        # Base congestion score
        score = 0
        
        # Distance factor
        if distance > 20:
            score += 2
        elif distance > 10:
            score += 1
        
        # Time factor
        if 8 <= hour <= 10 or 17 <= hour <= 19:  # Peak hours
            score += 2
        elif 7 <= hour <= 11 or 16 <= hour <= 20:  # Extended peak
            score += 1
        
        # Day factor
        if weekday in [5, 6]:  # Weekend
            score += 1
        
        # Weather factor
        if weather in ['Rain', 'Thunderstorm']:
            score += 1
        
        # Event factor
        if event:
            score += 1
        
        # Determine congestion level
        if score >= 4:
            congestion = 'High'
        elif score >= 2:
            congestion = 'Medium'
        else:
            congestion = 'Low'
        
        # Generate probabilities
        if congestion == 'High':
            probabilities = [0.1, 0.2, 0.7]
        elif congestion == 'Medium':
            probabilities = [0.2, 0.6, 0.2]
        else:
            probabilities = [0.7, 0.2, 0.1]
        
        return congestion, probabilities
    
    def suggest_mode(self, congestion_level, distance):
        """Suggest transport mode based on congestion and distance"""
        if distance <= 2:
            return 'Walk'
        elif distance <= 8:
            if congestion_level == 'High':
                return 'Metro'
            else:
                return 'Bike'
        else:
            if congestion_level == 'High':
                return 'Metro'
            else:
                return 'Car'
    
    def predict_traffic(self, city, source, destination):
        """Main prediction method"""
        # Get coordinates
        source_lat, source_lon = self.get_coordinates(source)
        dest_lat, dest_lon = self.get_coordinates(destination)
        
        # Calculate distance
        distance = self.calculate_distance(source_lat, source_lon, dest_lat, dest_lon)
        
        # Get current time
        now = datetime.now()
        hour = now.hour
        weekday = now.weekday()
        
        # Determine day type
        if now.date() in self.india_holidays:
            day_type = 'holiday'
        elif weekday in [5, 6]:
            day_type = 'weekend'
        else:
            day_type = 'weekday'
        
        # Get weather
        weather = self.get_weather_data(city)
        
        # Get event flag
        event_flag = self.get_event_flag(hour, weekday)
        
        # Get route type
        route_type = self.get_route_type(distance)
        
        # Prepare features
        features = {
            'city': city,
            'distance_km': distance,
            'hour': hour,
            'weekday': weekday,
            'day_type': day_type,
            'weather': weather,
            'event': event_flag,
            'route_type': route_type
        }
        
        # Make prediction
        congestion_level, probabilities = self.predict_congestion(features)
        
        # Suggest mode
        suggested_mode = self.suggest_mode(congestion_level, distance)
        
        return {
            'congestion_level': congestion_level,
            'suggested_mode': suggested_mode,
            'probabilities': probabilities,
            'features': features,
            'coordinates': {
                'source': (source_lat, source_lon),
                'destination': (dest_lat, dest_lon)
            }
        }


# Global instance
predictor = TrafficPredictor() 