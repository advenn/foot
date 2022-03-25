from django.contrib.auth.models import User
from django.db import models


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

    class Meta:
        verbose_name_plural = "Upcoming Matches"


class Predict(models.Model):
    """Create predictor for upcoming match"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(UpcomingMatch, on_delete=models.CASCADE,)
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return self.match.home_team + " vs " + self.match.away_team


class TrueScore(models.Model):
    """Create true score for upcoming match"""
    match = models.ForeignKey(UpcomingMatch, on_delete=models.CASCADE, unique=True)
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(null=True, auto_now_add=True)
    home_prop_score = models.IntegerField(blank=True, null=True)
    away_prop_score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.match.home_team + f" {self.home_score}:{self.away_score} " + self.match.away_team


class Rate(models.Model):
    """We submit the true results of games, then check the predicts with this score,
     if the prediction is exact match we add 2 points to that user,
     if the proportional score is exact match we add 1 point to that user
     """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(TrueScore, on_delete=models.CASCADE)
    score = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} rate {self.match.home_score} vs {self.match.away_score} {self.score}"
