#!/usr/bin/env python
"""
Script pour nettoyer les tentatives de quiz corrompues ou en double
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nird_Quiz.settings')
django.setup()

from NIRD.models import UserQuizAttempt, UserAnswer
from django.contrib.auth.models import User

def cleanup_attempts():
    """Nettoie les tentatives de quiz problématiques"""
    
    print("🧹 Nettoyage des tentatives de quiz...")
    print("─" * 60)
    
    # 1. Supprimer les tentatives non complétées
    incomplete_attempts = UserQuizAttempt.objects.filter(completed=False)
    count = incomplete_attempts.count()
    if count > 0:
        print(f"📋 Suppression de {count} tentatives non complétées...")
        incomplete_attempts.delete()
        print(f"✅ {count} tentatives supprimées")
    else:
        print("✅ Aucune tentative non complétée à supprimer")
    
    # 2. Recalculer les scores pour toutes les tentatives complétées
    print("\n📊 Recalcul des scores...")
    completed_attempts = UserQuizAttempt.objects.filter(completed=True)
    
    for attempt in completed_attempts:
        # Recalculer le score basé sur les réponses correctes
        correct_answers = attempt.answers.filter(correct=True)
        new_score = sum(answer.question.points for answer in correct_answers)
        
        if attempt.score != new_score:
            print(f"   🔧 {attempt.user.username} - {attempt.quiz.title}: {attempt.score} → {new_score} points")
            attempt.score = new_score
            attempt.save()
    
    print("✅ Scores recalculés")
    
    # 3. Mettre à jour les stats de tous les profils
    print("\n👥 Mise à jour des profils utilisateurs...")
    users = User.objects.all()
    
    for user in users:
        if hasattr(user, 'profile'):
            old_points = user.profile.total_points
            old_level = user.profile.level
            user.profile.update_stats()
            
            if old_points != user.profile.total_points or old_level != user.profile.level:
                print(f"   🔧 {user.username}: Niveau {old_level} → {user.profile.level}, {old_points} → {user.profile.total_points} points")
    
    print("✅ Profils mis à jour")
    
    # 4. Statistiques finales
    print("\n" + "=" * 60)
    print("📊 STATISTIQUES FINALES")
    print("=" * 60)
    print(f"   • Tentatives complétées : {UserQuizAttempt.objects.filter(completed=True).count()}")
    print(f"   • Tentatives en cours : {UserQuizAttempt.objects.filter(completed=False).count()}")
    print(f"   • Réponses totales : {UserAnswer.objects.count()}")
    print(f"   • Utilisateurs : {User.objects.count()}")
    print()
    print("✨ Nettoyage terminé avec succès !")
    print()

if __name__ == "__main__":
    cleanup_attempts()
