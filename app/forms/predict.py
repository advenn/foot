from wtforms import HiddenField, StringField, BooleanField, IntegerField, SelectField, validators, DateTimeField
from wtforms.validators import DataRequired
import datetime
from wtformsblacksheep import BlacksheepForm


class PredictForm(BlacksheepForm):
    user = HiddenField('user', validators=[DataRequired()])
    match = HiddenField('match', validators=[DataRequired()])
    home_score = IntegerField('home_score', validators=[DataRequired()])
    away_score = IntegerField('away_score', validators=[DataRequired()])


class TourForm(BlacksheepForm):
    number = IntegerField('number', validators=[DataRequired()])
    is_active = BooleanField('is_active', validators=[DataRequired()])
    start_time = DateTimeField('start_time', validators=[DataRequired()])
    deadline = DateTimeField('deadline', validators=[DataRequired()])


class UserForm(BlacksheepForm):
    name = StringField('name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    # created_at = HiddenField('created_at', validators=[DataRequired()])


class UpcomingMatchForm(BlacksheepForm):
    user = HiddenField('user', validators=[DataRequired()])
    tour = HiddenField('tour', validators=[DataRequired()])
    home_score = IntegerField('home_score', validators=[DataRequired()])
    away_score = IntegerField('away_score', validators=[DataRequired()])


class TrueScoreForm(BlacksheepForm):
    match = SelectField('match', validators=[DataRequired()])
    home_score = IntegerField('home_score', validators=[DataRequired()])
    away_score = IntegerField('away_score', validators=[DataRequired()])
    date = DateTimeField('date', validators=[DataRequired()], default=datetime.datetime.now())
    proportional_score = IntegerField('proportional_score', validators=[DataRequired()])
    is_counted = BooleanField('is_counted', validators=[DataRequired()], default=False)