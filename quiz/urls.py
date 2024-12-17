from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('start/', views.start_quiz, name='start_quiz'),
    path('question/', views.fetch_question, name='fetch_question'),
    path('submit/', views.submit_answer, name='submit_answer'),
    path('summary/', views.quiz_summary, name='summary'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
