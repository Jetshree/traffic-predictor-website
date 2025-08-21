from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import random
import requests
from datetime import datetime, timedelta

from .models import Prediction, SavedScenario
from .services.model import predictor


def home(request):
    """Home page with hero section and feature cards"""
    return render(request, 'predictor/home.html')


def predict_view(request):
    """Main prediction page"""
    cities = ['Delhi', 'Mumbai', 'Bengaluru', 'Hyderabad', 'Chennai', 'Kolkata']
    
    if request.method == 'POST':
        city = request.POST.get('city')
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        
        if city and source and destination:
            # Make prediction
            result = predictor.predict_traffic(city, source, destination)
            
            # Save prediction to database
            prediction = Prediction.objects.create(
                user=request.user if request.user.is_authenticated else None,
                city=city,
                source=source,
                destination=destination,
                source_lat=result['coordinates']['source'][0],
                source_lon=result['coordinates']['source'][1],
                dest_lat=result['coordinates']['destination'][0],
                dest_lon=result['coordinates']['destination'][1],
                distance_km=result['features']['distance_km'],
                hour=result['features']['hour'],
                weekday=result['features']['weekday'],
                day_type=result['features']['day_type'],
                weather=result['features']['weather'],
                event_flag=result['features']['event'],
                route_type=result['features']['route_type'],
                congestion_level=result['congestion_level'],
                suggested_mode=result['suggested_mode']
            )
            
            context = {
                'cities': cities,
                'prediction': prediction,
                'result': result,
                'show_result': True
            }
        else:
            messages.error(request, 'Please fill in all fields.')
            context = {'cities': cities}
    else:
        context = {'cities': cities}
    
    return render(request, 'predictor/predict.html', context)


@csrf_exempt
def predict_ajax(request):
    """AJAX endpoint for predictions"""
    if request.method == 'POST':
        data = json.loads(request.body)
        city = data.get('city')
        source = data.get('source')
        destination = data.get('destination')
        
        if city and source and destination:
            result = predictor.predict_traffic(city, source, destination)
            return JsonResponse(result)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def news_view(request):
    """Traffic news page"""
    cities = ['Delhi', 'Mumbai', 'Bengaluru', 'Hyderabad', 'Chennai', 'Kolkata']
    selected_city = request.GET.get('city', 'Delhi')
    
    # Try to fetch news from NewsAPI
    news_articles = []
    try:
        # You can add your NewsAPI key here
        api_key = "your_newsapi_key"  # Replace with actual key
        query = f"traffic {selected_city}"
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={api_key}"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            news_articles = data.get('articles', [])[:10]
        else:
            raise Exception("API request failed")
    except Exception as e:
        print(f"News API error: {e}")
        # Fallback: generate synthetic news
        news_articles = generate_synthetic_news(selected_city)
    
    context = {
        'cities': cities,
        'selected_city': selected_city,
        'news_articles': news_articles
    }
    return render(request, 'predictor/news.html', context)


def generate_synthetic_news(city):
    """Generate synthetic traffic news when API is unavailable"""
    headlines_and_content = [
        {
            'title': f"Traffic congestion expected on major roads in {city} during peak hours",
            'content': f"Commuters in {city} are advised to plan their journeys carefully as traffic congestion is expected on major arterial roads during peak hours today. The traffic police have identified several bottlenecks including main intersections and highway entry points. Alternative routes are recommended for faster travel."
        },
        {
            'title': f"New metro line to reduce traffic in {city} by 30%",
            'content': f"The newly inaugurated metro line in {city} is expected to significantly reduce road traffic by up to 30% according to transport authorities. The line connects major commercial and residential areas, providing commuters with a faster and more reliable alternative to road transport."
        },
        {
            'title': f"Smart traffic signals installed across {city} to improve flow",
            'content': f"The {city} municipal corporation has installed AI-powered smart traffic signals at 50 major intersections. These signals adapt to real-time traffic conditions and are expected to reduce waiting times by 25% and improve overall traffic flow throughout the city."
        },
        {
            'title': f"Construction work on {city} highways may cause delays",
            'content': f"Ongoing construction work on major highways in {city} may cause significant delays for commuters over the next two weeks. The public works department advises using alternative routes and allowing extra travel time. Work is being conducted during off-peak hours where possible."
        },
        {
            'title': f"Traffic police launch new initiative to reduce congestion in {city}",
            'content': f"The {city} traffic police have launched a comprehensive initiative to tackle traffic congestion. The program includes deployment of additional personnel at key intersections, improved signal timing, and a public awareness campaign about traffic rules and safe driving practices."
        },
        {
            'title': f"Public transport usage increases in {city} as fuel prices rise",
            'content': f"With rising fuel prices, more commuters in {city} are switching to public transport. Bus ridership has increased by 15% over the past month, while metro usage has grown by 20%. Transport authorities are considering increasing service frequency to meet growing demand."
        },
        {
            'title': f"New flyover project to ease traffic in {city} city center",
            'content': f"A new flyover project in {city} city center is set to begin next month. The project aims to reduce traffic congestion at one of the busiest intersections in the city. The flyover is expected to be completed within 18 months and will significantly improve traffic flow."
        },
        {
            'title': f"Traffic advisory issued for {city} due to upcoming festival",
            'content': f"The {city} traffic police have issued an advisory for the upcoming festival celebrations. Several roads will be closed or have restricted access. Commuters are advised to use public transport and avoid the city center during festival hours. Additional parking arrangements have been made."
        },
        {
            'title': f"Bike lanes to be expanded across {city} to promote cycling",
            'content': f"The {city} municipal corporation has announced plans to expand dedicated bike lanes across the city. The initiative aims to promote cycling as an eco-friendly mode of transport and reduce vehicular traffic. The project will cover 100 kilometers of roads over the next year."
        },
        {
            'title': f"Traffic monitoring system upgraded in {city} with AI technology",
            'content': f"The traffic monitoring system in {city} has been upgraded with artificial intelligence technology. The new system can predict traffic patterns, detect accidents in real-time, and automatically adjust signal timings. This is expected to reduce travel time by up to 20%."
        }
    ]
    
    sources = ['Times of India', 'Hindustan Times', 'The Hindu', 'Economic Times', 'Indian Express']
    
    news_articles = []
    for i, article_data in enumerate(headlines_and_content):
        news_articles.append({
            'title': article_data['title'],
            'content': article_data['content'],
            'source': {'name': random.choice(sources)},
            'url': f"/news/article/{i+1}/",
            'publishedAt': (datetime.now() - timedelta(days=random.randint(1, 7))).isoformat()
        })
    
    return news_articles


def news_article_detail(request, article_id):
    """Display individual news article"""
    # Get the synthetic news articles
    news_articles = generate_synthetic_news("Delhi")  # Default city for article lookup
    
    try:
        article_index = int(article_id) - 1
        if 0 <= article_index < len(news_articles):
            article = news_articles[article_index]
            context = {
                'article': article,
                'article_id': article_id
            }
            return render(request, 'predictor/news_detail.html', context)
        else:
            raise ValueError("Article not found")
    except (ValueError, IndexError):
        messages.error(request, 'Article not found.')
        return redirect('news')


@login_required
def dashboard_view(request):
    """User dashboard with recent predictions and charts"""
    # Get user's recent predictions
    recent_predictions = Prediction.objects.filter(user=request.user)[:10]
    
    # Get saved scenarios
    saved_scenarios = SavedScenario.objects.filter(user=request.user)[:5]
    
    # Calculate congestion statistics based on actual predictions
    all_user_predictions = Prediction.objects.filter(user=request.user)
    total_predictions = all_user_predictions.count()
    low_congestion = all_user_predictions.filter(congestion_level='Low').count()
    medium_congestion = all_user_predictions.filter(congestion_level='Medium').count()
    high_congestion = all_user_predictions.filter(congestion_level='High').count()
    
    # Generate chart data
    chart_data = generate_chart_data()
    
    context = {
        'recent_predictions': recent_predictions,
        'saved_scenarios': saved_scenarios,
        'chart_data': chart_data,
        'total_predictions': total_predictions,
        'low_congestion': low_congestion,
        'medium_congestion': medium_congestion,
        'high_congestion': high_congestion,
    }
    return render(request, 'predictor/dashboard.html', context)


def generate_chart_data():
    """Generate synthetic chart data for dashboard"""
    # Peak hour trend data
    hours = list(range(24))
    congestion_levels = []
    for hour in hours:
        if 8 <= hour <= 10 or 17 <= hour <= 19:
            congestion_levels.append(random.randint(70, 90))
        elif 7 <= hour <= 11 or 16 <= hour <= 20:
            congestion_levels.append(random.randint(50, 70))
        else:
            congestion_levels.append(random.randint(20, 50))
    
    # Route type congestion data
    route_types = ['Local', 'Suburban', 'Highway']
    route_congestion = [random.randint(60, 80), random.randint(40, 60), random.randint(30, 50)]
    
    return {
        'peak_hours': {
            'labels': hours,
            'data': congestion_levels
        },
        'route_types': {
            'labels': route_types,
            'data': route_congestion
        }
    }


def about_view(request):
    """About page with ML workflow explanation"""
    return render(request, 'predictor/about.html')


def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'predictor/register.html', {'form': form})


@login_required
def save_scenario(request):
    """Save a prediction scenario"""
    if request.method == 'POST':
        name = request.POST.get('name')
        city = request.POST.get('city')
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        
        if name and city and source and destination:
            SavedScenario.objects.create(
                user=request.user,
                name=name,
                city=city,
                source=source,
                destination=destination
            )
            messages.success(request, 'Scenario saved successfully!')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return redirect('dashboard')


@login_required
def delete_scenario(request, scenario_id):
    """Delete a saved scenario"""
    try:
        scenario = SavedScenario.objects.get(id=scenario_id, user=request.user)
        scenario.delete()
        messages.success(request, 'Scenario deleted successfully!')
    except SavedScenario.DoesNotExist:
        messages.error(request, 'Scenario not found.')
    
    return redirect('dashboard')
