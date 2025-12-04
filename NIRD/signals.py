from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Quiz, Question

@receiver(post_migrate)
def create_default_questions(sender, **kwargs):
    # Ici tu vas mettre le code qui ajoute tes questions par défaut
    pass
