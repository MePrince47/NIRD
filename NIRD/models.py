from django.db import models
from django.db.models import JSONField


class Quiz(models.Model):
 
    title = models.CharField(max_length=255)
    level = models.PositiveIntegerField(default=1)  # Niveau du quiz (1,2,3...)

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
