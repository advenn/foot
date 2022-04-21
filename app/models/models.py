from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    username: str
    name: str
    email: str
    password: str
    created_at: datetime


class Tour(BaseModel):
    number: int
    is_active: bool
    start_time: datetime
    deadline: datetime

    def __str__(self):
        return str(self.number)


class UpcomingMatch(BaseModel):
    """Create upcoming match, predictors predict for this model"""
    tour: Tour
    home_team: str
    away_team: str

    def __str__(self):
        return self.home_team + " vs " + self.away_team


class Predict(BaseModel):
    """Create predictor for upcoming match"""
    user: int
    match: UpcomingMatch
    home_score: int
    away_score: int
    date: datetime

    def __str__(self):
        return self.match.home_team + " vs " + self.match.away_team


class TrueScore(BaseModel):
    """Create true score for upcoming match"""
    match: UpcomingMatch
    home_score: int
    away_score: int
    date: datetime
    proportional_score: int
    is_counted: bool

    def __str__(self):
        return self.match.home_team + f" {self.home_score}:{self.away_score} " + self.match.away_team


class Rate(BaseModel):
    """We submit the true results of games, then check the predicts with this score,
     if the prediction is exact match we add 2 points to that user,
     if the proportional score is exact match we add 1 point to that user
     """
    user: User
    score: int
    date: datetime

    def __str__(self):
        return f"{self.user.username}'s rating: {self.score}"

