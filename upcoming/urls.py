from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', main, name='dashboard'),
    path('register', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('predict/', predict_receive, name='predict_receive'),
    path('edit/<int:predict_id>', edit, name='edit'),
    path('edit_predict/', edit_predict, name='edit_predict'),
    path('finished-games/', finished_games, name='finished_games'),
    path('check_preds/', check_scores_after_match, name='check_preds'),

]