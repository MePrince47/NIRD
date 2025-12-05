from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import User




class Quiz(models.Model):
 
    title = models.CharField(max_length=255)
    level = models.PositiveIntegerField(default=1)  

    def __str__(self):
        return f"{self.title} (Niveau {self.level})"


class Question(models.Model):
 
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
        db_index=True
    )

    text = models.TextField()  # Le texte de la question

    answers = JSONField(default=list)
    correct_index = models.PositiveIntegerField(default=0) 
    order = models.PositiveIntegerField(default=0, db_index=True)
    points = models.PositiveIntegerField(default=1)
    time_limit = models.PositiveIntegerField(default=30)

    def is_correct(self, answer_index: int) -> bool:
        """Vérifie si la réponse envoyée est correcte."""
        return answer_index == self.correct_index

    def __str__(self):
        return f"{self.text[:50]}"


class UserQuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    selected_questions = models.JSONField(default=list)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

class UserAnswer(models.Model):
    attempt = models.ForeignKey(UserQuizAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_index = models.PositiveIntegerField()
    correct = models.BooleanField(default=False)