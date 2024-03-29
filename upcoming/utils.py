import sqlite3

import numpy as np
import telebot

from .models import *

bot = telebot.TeleBot('5160879108:AAFe5QrI8ZOGBZkDvxESb5V8qPg5I-zCBco')
LOG_GROUP_ID = '-653199381'


def prop(x):
    minimum = x.min()
    new = x - np.array([minimum])
    return new


def get_scores():
    """Get predicts of related match"""
    conn = sqlite3.connect('../db.sqlite3')
    cursor = conn.cursor()
    last_tour = Tour.objects.last()
    preds = Predict.objects.filter(match__tour=last_tour).values_list('user', 'home_score', 'away_score')

    cursor.execute("SELECT * FROM predict_predict WHERE tour_number = ?", (last_tour,))


# def check_scores_and_rate(match_details):
#     match_id = match_details['match_id']
#     home_score = match_details['home_score']
#     away_score = match_details['away_score']
#     home_prop_score = match_details['home_prop_score']
#     away_prop_score = match_details['away_prop_score']
#     predicts = Predict.objects.filter(match__id=match_id)
#     preds = pd.DataFrame(data=list(predicts.values('user', 'home_score', 'away_score')))
#     props = np.array([prop(np.array([x[2], x[3]])) for x in preds.itertuples()])
#     # true_scores = np.array([[home_score, away_score, home_prop_score, away_prop_score]])
#     actual = np.array([match_details['home_score'], match_details['away_score']])
#     proportion = actual - min(actual)
#     preds['prop_home'] = props[:, 0]
#     preds['away_prop'] = props[:, 1]
#     exact_match = preds[(preds['home_score'] == actual[0]) & (preds['away_score'] == actual[1])]
#     proportional_match = preds[(preds['prop_home'] == proportion[0]) & (preds['away_prop'] == proportion[1])]
#     if exact_match.shape[0] > 0:
#         for i in exact_match.itertuples():
#             user = User.objects.get(id=i[1])
#             user.score += 2
#             user.save()
#     elif proportional_match.shape[0] > 0:
#         for i in proportional_match.itertuples():
#             user = User.objects.get(id=i[1])
#             user.score += 1
#             user.save()
#     if exact_match.shape[0] > 0 or proportional_match.shape[0] > 0:
#         return True
#     return False
# rate = Rate()
# user_id = exact_match['user']
# rate.user = exact_match.user
# return exact_match, proportional_match
# print(exact_match, proportional_match, actual, preds, sep='\n')


def check_scores_and_rate(match_details: TrueScore):
    match = match_details
    if match:
        predicts = Predict.objects.filter(match__id=match_details.match_id)
        home_score = match_details.home_score
        away_score = match_details.away_score
        count = 0
        for predict in predicts:
            user, home, away = predict.user, predict.home_score, predict.away_score
            result = 0
            if int(home) == int(home_score) and int(away) == int(away_score):
                result = 2
            elif home == home_score or away == away_score:
                result = 1
            else:
                result = 0
            if bool(result):
                rate = Rate()
                rate.user = user
                rate.score = int(result)
                rate.match = match.match
                rate.predict = predict
                rate.save()
            count += 1
        match.is_counted = True
        match.save()
        return True, count
