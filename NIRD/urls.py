from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Pages principales
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Quiz
    path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('attempt/<int:attempt_id>/question/<int:question_id>/', views.question_view, name='question'),
    path('attempt/<int:attempt_id>/result/', views.quiz_result, name='quiz_result'),
    
    # Réseau social
    path('social/', views.social_feed, name='social_feed'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.comment_post, name='comment_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    
    # Classement et profils
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
]
