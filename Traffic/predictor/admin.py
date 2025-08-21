from django.contrib import admin
from .models import Prediction, SavedScenario


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['city', 'source', 'destination', 'congestion_level', 'suggested_mode', 'created_at', 'user']
    list_filter = ['city', 'congestion_level', 'suggested_mode', 'day_type', 'weather', 'created_at']
    search_fields = ['city', 'source', 'destination']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'city', 'source', 'destination', 'created_at')
        }),
        ('Coordinates', {
            'fields': ('source_lat', 'source_lon', 'dest_lat', 'dest_lon', 'distance_km')
        }),
        ('Features', {
            'fields': ('hour', 'weekday', 'day_type', 'weather', 'event_flag', 'route_type')
        }),
        ('Prediction Results', {
            'fields': ('congestion_level', 'suggested_mode')
        }),
    )


@admin.register(SavedScenario)
class SavedScenarioAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'source', 'destination', 'user', 'created_at']
    list_filter = ['city', 'created_at']
    search_fields = ['name', 'city', 'source', 'destination', 'user__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
