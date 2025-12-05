from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('start_quiz/<int:level>/', views.start_quiz, name='start_quiz'),
    path('question/<int:attempt_id>/<int:question_id>/', views.question_view, name='question'),
    path('result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    path('signup/', views.signup, name='signup'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('chat/', views.chat_view, name='chat'),
    path('progression/', views.progression, name='progression'),
    path('', views.viewsroad, name='road'),
]
