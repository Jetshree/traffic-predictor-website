from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('predict/', views.predict_view, name='predict'),
    path('news/', views.news_view, name='news'),
    path('news/article/<int:article_id>/', views.news_article_detail, name='news_detail'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('about/', views.about_view, name='about'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='predictor/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # AJAX endpoints
    path('predict-ajax/', views.predict_ajax, name='predict_ajax'),
    
    # User actions
    path('save-scenario/', views.save_scenario, name='save_scenario'),
    path('delete-scenario/<int:scenario_id>/', views.delete_scenario, name='delete_scenario'),
] 