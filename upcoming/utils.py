import sqlite3
from models import *

def get_scores():
    """Get predicts of related match"""
    conn = sqlite3.connect('../db.sqlite3')
    cursor = conn.cursor()
    last_tour = Tour.objects.last()
    preds = Predict.objects.filter(match__tour=last_tour).values_list('user', 'home_score', 'away_score')


    cursor.execute("SELECT * FROM predict_predict WHERE tour_number = ?", (last_tour,))
