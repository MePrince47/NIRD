from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('attempt/<int:attempt_id>/question/<int:question_id>/', views.question_view, name='question'),
    path('attempt/<int:attempt_id>/result/', views.quiz_result, name='quiz_result'),
]
