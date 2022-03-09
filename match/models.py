from django.db import models
from django.models.user import User

class User(User):
    pass

class Tour(models.Model):
    number = models.IntegerField()
    league = models.ForeignKey(to="League", on_delete=models.CASCADE)

    def __str__(self):
        return f"tour of {self.number} on {self.league}"

class U:
    pass

class League(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    tour = models.ForeignKey(to="Tour", on_delete=models.CASCADE)
    league = models.ForeignKey(to="League", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date} at {self.date.strftime('%H:%M')}"


class Predict(models.Model):
    match = models.ForeignKey('Game', on_delete=models.CASCADE)
    # user = 
    # def __str__(self):
    #     return f"{self.home_team} vs {self.away_team} on {self.date} at {self.date.strftime('%H:%M')}"