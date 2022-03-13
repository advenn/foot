from django.db import models


class League(models.Model): 
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tour(models.Model):
    number = models.IntegerField()
    league = models.ForeignKey(to="League", on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    start_time = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return str(self.number) + " - " + self.league.name



class UpcomingMatch(models.Model):
    """Create upcoming match, predictors predict for this model"""
    home_team = models.CharField(max_length=40)
    away_team = models.CharField(max_length=40)
    matchdate = models.DateTimeField()
    # tour = models.IntegerField()

    def __str__(self):
        return self.home_team + " vs " + self.away_team  + " on " + self.matchdate.strftime('%d.%m.%Y')


class Predict(models.Model):
    """Create predictor for upcoming match"""
    match = models.ForeignKey(to="UpcomingMatch", on_delete=models.CASCADE)
    # user = models.ForeignKey(to="User", on_delete=models.CASCADE)
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.match.home_team + " vs " + self.match.away_team

