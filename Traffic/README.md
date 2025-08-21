# Traffic Congestion Predictor

A production-quality web application that predicts traffic congestion in real-time using advanced machine learning algorithms. Built with Django, Tailwind CSS, HTMX, Chart.js, and Folium.

## 🚀 Features

### Core Functionality
- **Real-time Traffic Prediction**: Get instant congestion forecasts for major Indian cities
- **Interactive Maps**: Visualize routes with detailed maps and congestion overlays
- **Transport Mode Suggestions**: Get personalized recommendations for optimal transport
- **Data Visualization**: Comprehensive charts and graphs for traffic analysis
- **Traffic News Integration**: Stay updated with latest traffic news and alerts
- **User Dashboard**: Track prediction history and save favorite routes

### Technical Features
- **Machine Learning Engine**: Advanced ML algorithms with fallback prediction logic
- **Geocoding Integration**: Automatic coordinate fetching via Nominatim API
- **Weather Integration**: Real-time weather data via OpenWeather API
- **Responsive Design**: Mobile-first design with Tailwind CSS
- **Interactive Charts**: Chart.js integration for data visualization
- **HTMX Integration**: Dynamic updates without page refreshes

## 🛠️ Technology Stack

### Backend
- **Django 5.0.2**: Python web framework
- **scikit-learn**: Machine learning library
- **SQLite**: Database
- **Geopy**: Geocoding and distance calculations
- **Folium**: Interactive maps
- **Holidays**: Holiday detection for India

### Frontend
- **Tailwind CSS**: Utility-first CSS framework
- **HTMX**: Dynamic HTML updates
- **Chart.js**: Data visualization
- **Leaflet.js**: Interactive maps
- **Responsive Design**: Mobile-first approach

### APIs & Services
- **Nominatim**: Geocoding service
- **OpenWeather API**: Weather data
- **NewsAPI**: Traffic news (optional)

## 📋 Prerequisites

- Python 3.10+
- pip (Python package installer)
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Traffic
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install django==5.0.2 scikit-learn folium holidays requests geopy
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Create Sample ML Model
```bash
python create_sample_model.py
```

### 7. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 8. Run the Development Server
```bash
python manage.py runserver
```

### 9. Access the Application
Open your browser and navigate to:
- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📱 Usage Guide

### Making Predictions
1. Navigate to the **Predict** page
2. Select a city from the dropdown
3. Enter source and destination locations
4. Click "Predict Traffic" to get results
5. View detailed analysis with charts and maps

### User Features
- **Register/Login**: Create an account to save predictions
- **Dashboard**: View your prediction history and saved scenarios
- **News**: Browse traffic news by city
- **About**: Learn about the ML workflow and technology stack

### Admin Features
- Access admin panel at `/admin/`
- Manage predictions and saved scenarios
- View user data and system statistics

## 🏗️ Project Structure

```
Traffic/
├── traffic_predictor/          # Django project settings
├── predictor/                  # Main application
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── urls.py                # URL routing
│   ├── admin.py               # Admin configuration
│   └── services/              # Business logic
│       └── model.py           # ML prediction service
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   └── predictor/            # App-specific templates
├── static/                   # Static files
├── traffic_model.pkl         # ML model file
├── create_sample_model.py    # Model creation script
├── manage.py                 # Django management
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables
The application works without API keys but can be enhanced with:

```bash
# Optional: OpenWeather API Key
OPENWEATHER_API_KEY=your_api_key_here

# Optional: NewsAPI Key
NEWSAPI_KEY=your_api_key_here
```

### Model Configuration
- The application includes a sample ML model (`traffic_model.pkl`)
- Replace with your trained model for production use
- Model expects features: `["city", "distance_km", "hour", "weekday", "day_type", "weather", "event", "route_type"]`

## 🎯 Supported Cities

- Delhi
- Mumbai
- Bengaluru
- Hyderabad
- Chennai
- Kolkata

## 📊 ML Features

### Input Features
- **City**: Target city for prediction
- **Distance**: Calculated using Haversine formula
- **Time**: Current hour (0-23)
- **Day Type**: weekday/weekend/holiday
- **Weather**: Current weather conditions
- **Events**: Special events flag
- **Route Type**: local/suburban/highway

### Output
- **Congestion Level**: Low/Medium/High
- **Suggested Mode**: Car/Metro/Bike/Walk
- **Confidence Scores**: Probability distribution

## 🚀 Deployment

### Production Setup
1. Set `DEBUG = False` in settings.py
2. Configure a production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure environment variables
5. Use a production WSGI server (Gunicorn)

### Docker Deployment
```bash
# Build and run with Docker
docker build -t traffic-predictor .
docker run -p 8000:8000 traffic-predictor
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code comments

## 🔮 Future Enhancements

- Real-time traffic data integration
- Mobile app development
- Advanced ML models
- Multi-language support
- API endpoints for third-party integration
- Real-time notifications
- Route optimization algorithms

---

**Built with ❤️ using Django, Tailwind, and Machine Learning** 