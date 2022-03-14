from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['number', 'is_active', 'start_time', 'deadline']

@admin.register(Predict)
class PredictAdmin(admin.ModelAdmin):
    list_display = ['match', 'home_score', 'away_score', 'date', 'user']
    list_filter = ['user']

@admin.register(UpcomingMatch)
class UpcomingMatchAdmin(admin.ModelAdmin):
    list_display = ['home_team', 'away_team', 'tour']