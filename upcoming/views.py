from django.shortcuts import render, HttpResponse
from .models import UpcomingMatch, Predict
import datetime
from django.http import JsonResponse
import pandas as pd


def main(request):
    queryset = UpcomingMatch.objects.filter(matchdate__gt=datetime.datetime.today())
    print(queryset)
    context = {
        'upcoming':queryset,
        'title':"predict",
    }

    return render(request, 'form.html', context=context)


def predict_receive(request):
    # print(request.__dict__)
    post = request.POST
    myDict = dict(post.dict())
    del myDict['csrfmiddlewaretoken']
    print(myDict)
    games = []
    for key, value in myDict.items():
        match_id = key.split('_')[1]
        h_or_a = key.split('_')[2]
        state = ""
        if h_or_a == 'h':
            state = 'home'
        else:
            state = 'away'
        game = [match_id, state, value]
        games.append(game)
        # home, away = value.split(':')
        # match = UpcomingMatch.objects.get(id=int(match_id))
        # predict = Predict()
        # predict.match = match
        # predict.home_score = int(home)
        # predict.away_score = int(away)
        # predict.save()
        print(key, value)
    df = pd.DataFrame(games, columns=['match_id', 'state', 'score']) 
    uniques = df.match_id.unique()
    upcmatches = UpcomingMatch.objects.filter(id__in=uniques)
    for match_id in uniques:
        match = upcmatches.get(id=int(match_id))
        scores = df[df.match_id == match_id].score.values
        home, away = scores[0], scores[1]
        predict = Predict()
        predict.match = match
        predict.home_score = int(home)
        predict.away_score = int(away)
        predict.save()
    user = request.user
    print(df, user)
    return HttpResponse(request.POST)

 