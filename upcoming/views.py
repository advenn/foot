from django.shortcuts import render, HttpResponse
from .models import UpcomingMatch, Predict, Tour, TrueScore, Rate
from django.contrib.auth.decorators import login_required
import pandas as pd
from .forms import UserRegistrationForm
import datetime


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
    msg = ''
    user = request.user
    tour = Tour.objects.filter(is_active=True, deadline__gt=datetime.datetime.now())
    if tour.count() == 0:
        return HttpResponse('''Ayni vaqtda aktiv holatdagi o\'yinlar mavjud emas!
       ''')

    matches = UpcomingMatch.objects.filter(tour__is_active=True, tour__deadline__gt=datetime.datetime.now())
    user_predicts = Predict.objects.filter(user=user)
    active_matches_list = matches.values_list('tour', flat=True)
    upcoming_matches = UpcomingMatch.objects.filter(tour__is_active=True)
    preds = Predict.objects.filter(user=user, match__tour__is_active=True)
    unsubmitted = upcoming_matches.exclude(id__in=preds)
    predicts = upcoming_matches.exclude(pk__in=user_predicts.values_list('match', flat=True))
    submitted = []
    not_submitted = []
    for upc in upcoming_matches:
        match = preds.filter(match=upc)
        if match.count() == 0:
            not_submitted.append(upc)
        else:
            submitted.append(upc)
    # print(submitted, not_submitted, preds, predicts)        
    context = {
        'title':'Taxmin qilish',
        'upcoming': not_submitted,
        'submitted': preds,
    }
    return render(request, template_name='account/dashboard.html', context=context)

    # if len(predicts) == 0:
    #     msg = 'Siz avvalroq joriy o\'yinlar uchun taxminingizni kiritgansiz!'
    #     status = 'already_submitted'
    #     return render(request, 'account/submitted.html',
    #     context={'msg': msg, 'status': status,'title':"Predict",
    #     'predicts':user_predicts, })
    # else:
    #     msg = 'not_submitted'
    #     status = 'not_submitted'

    # context = {
    #     'upcoming':predicts,
    #     'title':"Predict",
    # }

    # print(context)
    # return render(request, 'account/dashboard.html', context=context)


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
        if value == '':
            value = None
        game = [match_id, state, value]
        games.append(game)
    df = pd.DataFrame(games, columns=['match_id', 'state', 'score']) 
    df.dropna(axis=0, how='any', inplace=True)
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


@login_required
def edit(request, predict_id):
    predict = Predict.objects.get(id=int(predict_id))

    context = {
        "user":request.user,
        'title':'Taxminni tahrirlash',
        'predict': predict,
    }
    return render(request, 'account/edit_predict.html', context=context)

@login_required
def edit_predict(request):
    print(request.POST)
    user = request.user
    predict_pk = request.POST.get('pk')
    predict = Predict.objects.get(id=int(predict_pk), user=user)
    home_team = predict.match.home_team
    away_team = predict.match.away_team
    predict.home_score = request.POST.get('home_team')
    predict.away_score = request.POST.get('away_team')
    predict.save()
    print(user, predict_pk, request.POST.get('home_team'), request.POST.get('away_team'))
    return HttpResponse(f"Thanks, {user}!<br>Yangi taxmin: \
<t>    {home_team} {predict.home_score}:{predict.away_score} {away_team}</t>")


@login_required
def check_scores_after_match(request):
    user = request.user
    if user.is_superuser:
        finished_matches = TrueScore.objects.filter(match__n)
    predicts = Predict.objects.filter(user=user)
    for predict in predicts:
        if predict.match.is_finished:
            predict.home_score = predict.match.home_score
            predict.away_score = predict.match.away_score
            predict.save()
    return HttpResponse('Thanks')
