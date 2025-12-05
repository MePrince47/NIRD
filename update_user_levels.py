#!/usr/bin/env python
"""
Script pour recalculer les niveaux de tous les utilisateurs
avec le nouveau système de progression
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nird_Quiz.settings')
django.setup()

from django.contrib.auth.models import User
from NIRD.models import UserProfile

def update_all_user_levels():
    """Recalcule les niveaux de tous les utilisateurs"""
    
    print("🔄 Mise à jour des niveaux utilisateurs...")
    print("─" * 60)
    
    users = User.objects.all()
    updated_count = 0
    
    for user in users:
        if hasattr(user, 'profile'):
            old_level = user.profile.level
            old_points = user.profile.total_points
            
            # Recalculer les stats avec le nouveau système
            user.profile.update_stats()
            
            new_level = user.profile.level
            new_points = user.profile.total_points
            
            if old_level != new_level or old_points != new_points:
                print(f"✅ {user.profile.avatar_emoji} {user.username:15} | "
                      f"Niveau {old_level} → {new_level} | "
                      f"{old_points} → {new_points} points")
                updated_count += 1
            else:
                print(f"   {user.profile.avatar_emoji} {user.username:15} | "
                      f"Niveau {new_level} | {new_points} points (inchangé)")
    
    print()
    print("=" * 60)
    print(f"✨ Mise à jour terminée : {updated_count}/{users.count()} utilisateurs modifiés")
    print("=" * 60)
    print()
    
    # Afficher un résumé par niveau
    print("📊 Répartition par niveau :")
    for level in range(1, 7):
        count = UserProfile.objects.filter(level=level).count()
        if count > 0:
            bar = "█" * count
            print(f"   Niveau {level} : {bar} ({count} utilisateurs)")
    print()

if __name__ == "__main__":
    update_all_user_levels()
