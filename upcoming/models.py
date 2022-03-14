from django.db import models
from django.contrib.auth.models import User


class Tour(models.Model):
    number = models.IntegerField()
    is_active = models.BooleanField(default=False)
    start_time = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.number)


class UpcomingMatch(models.Model):
    """Create upcoming match, predictors predict for this model"""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='tur')
    home_team = models.CharField(max_length=40)
    away_team = models.CharField(max_length=40)

    def __str__(self):
        return self.home_team + " vs " + self.away_team


class Predict(models.Model):
    """Create predictor for upcoming match"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(UpcomingMatch, on_delete=models.CASCADE)
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return self.match.home_team + " vs " + self.match.away_team

