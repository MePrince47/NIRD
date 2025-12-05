from django.contrib import admin
from .models import (
    Quiz, Question, UserAnswer, UserQuizAttempt,
    QuizTip, UserProfile, Post, Comment, Like
)

# Configuration pour Quiz
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'level']
    list_filter = ['level']
    search_fields = ['title']

# Configuration pour Question
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'order', 'points']
    list_filter = ['quiz']
    search_fields = ['text']

# Configuration pour QuizTip
@admin.register(QuizTip)
class QuizTipAdmin(admin.ModelAdmin):
    list_display = ['icon', 'text', 'quiz', 'trigger_question_number']
    list_filter = ['quiz']
    search_fields = ['text']

# Configuration pour UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'total_points', 'avatar_emoji']
    list_filter = ['level']
    search_fields = ['user__username']

# Configuration pour Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'created_at', 'like_count', 'comment_count']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username']
    readonly_fields = ['created_at', 'updated_at']

# Configuration pour Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username']

# Configuration pour Like
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']

admin.site.register(UserQuizAttempt)
admin.site.register(UserAnswer)