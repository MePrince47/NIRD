from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import User
from django.utils import timezone




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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"


class UserAnswer(models.Model):
    attempt = models.ForeignKey(UserQuizAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_index = models.PositiveIntegerField()
    correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attempt.user.username} - Q{self.question.id}"


class QuizTip(models.Model):
    """Bulles d'info fun qui apparaissent pendant le quiz"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="tips")
    text = models.TextField(help_text="Conseil ou info fun à afficher")
    icon = models.CharField(max_length=10, default="💡", help_text="Emoji pour la bulle")
    trigger_question_number = models.PositiveIntegerField(
        default=1,
        help_text="Numéro de la question après laquelle afficher ce tip"
    )
    
    class Meta:
        ordering = ['trigger_question_number']
    
    def __str__(self):
        return f"{self.icon} {self.text[:50]}"


class UserProfile(models.Model):
    """Profil étendu pour les utilisateurs"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=500, blank=True, help_text="Bio de l'utilisateur")
    avatar_emoji = models.CharField(max_length=10, default="👤", help_text="Emoji avatar")
    total_points = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Niveau {self.level}"
    
    def update_stats(self):
        """Met à jour les statistiques de l'utilisateur"""
        attempts = UserQuizAttempt.objects.filter(user=self.user, completed=True)
        self.total_points = sum(attempt.score for attempt in attempts)
        
        # Calcul du niveau basé sur les quiz complétés avec succès
        # Un quiz est considéré réussi si le score >= 60% du maximum
        from NIRD.models import Quiz
        completed_quiz_levels = set()
        
        for attempt in attempts:
            quiz = attempt.quiz
            max_score = sum(q.points for q in quiz.questions.all())
            if max_score > 0:
                percentage = (attempt.score / max_score) * 100
                if percentage >= 60:  # 60% minimum pour valider un niveau
                    completed_quiz_levels.add(quiz.level)
        
        # Le niveau de l'utilisateur = le niveau le plus élevé complété + 1
        if completed_quiz_levels:
            self.level = max(completed_quiz_levels) + 1
        else:
            self.level = 1  # Niveau de départ
        
        self.save()
    
    def get_quiz_progress(self, quiz):
        """Retourne la progression de l'utilisateur pour un quiz donné"""
        attempts = UserQuizAttempt.objects.filter(
            user=self.user, 
            quiz=quiz, 
            completed=True
        ).order_by('-score')
        
        if not attempts.exists():
            return {
                'completed': False,
                'best_score': 0,
                'max_score': sum(q.points for q in quiz.questions.all()),
                'percentage': 0,
                'passed': False
            }
        
        best_attempt = attempts.first()
        max_score = sum(q.points for q in quiz.questions.all())
        percentage = (best_attempt.score / max_score * 100) if max_score > 0 else 0
        
        return {
            'completed': True,
            'best_score': best_attempt.score,
            'max_score': max_score,
            'percentage': round(percentage, 1),
            'passed': percentage >= 60
        }


class Post(models.Model):
    """Publications sur le réseau social NIRD"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=1000)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Lien optionnel vers un quiz
    related_quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="posts"
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author.username} - {self.content[:50]}"
    
    def like_count(self):
        return self.likes.count()
    
    def comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    """Commentaires sur les posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Pour les réponses aux commentaires
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.author.username} sur {self.post.id}: {self.content[:30]}"


class Like(models.Model):
    """Likes sur les posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f"{self.user.username} ❤️ Post {self.post.id}"