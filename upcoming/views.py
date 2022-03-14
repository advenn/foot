from django.shortcuts import render, HttpResponse
from .models import UpcomingMatch, Predict
from django.contrib.auth.decorators import login_required
import pandas as pd
from .forms import UserRegistrationForm


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def main(request):
    queryset = UpcomingMatch.objects.filter(tour__is_active=True)
    print(queryset)
    context = {
        'upcoming':queryset,
        'title':"predict",
    }

    return render(request, 'account/dashboard.html', context=context)


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
        predict.user = request.user
        predict.save()

    return HttpResponse('Thanks')

 