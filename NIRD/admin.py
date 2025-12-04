from django.contrib import admin

from .models import Quiz, Question, UserAnswer, UserQuizAttempt

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(UserQuizAttempt)
admin.site.register(UserAnswer)