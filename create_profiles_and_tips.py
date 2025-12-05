#!/usr/bin/env python
"""
Script combiné pour créer les profils utilisateurs et ajouter les tips
Exécutez ce script après avoir fait les migrations
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nird_Quiz.settings')
django.setup()

from django.contrib.auth.models import User
from NIRD.models import UserProfile, Quiz, QuizTip

def create_user_profiles():
    """Crée les profils pour tous les utilisateurs existants"""
    print("👤 Création des profils utilisateurs...")
    print("─" * 50)
    
    count = 0
    for user in User.objects.all():
        profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            count += 1
            print(f"✅ Profil créé pour {user.username}")
        else:
            print(f"ℹ️  Profil existe déjà pour {user.username}")
    
    if count > 0:
        print(f"\n✨ {count} nouveau(x) profil(s) créé(s)")
    else:
        print("\n✅ Tous les profils existent déjà")
    print()

def add_quiz_tips():
    """Ajoute les bulles d'info fun aux quiz"""
    print("💡 Ajout des bulles d'info fun aux quiz...")
    print("─" * 50)
    
    TIPS_DATA = {
        1: [
            {
                "icon": "💡",
                "text": "Saviez-vous ? En utilisant des logiciels libres, vous réduisez votre dépendance aux grandes entreprises tech !",
                "trigger": 2
            },
            {
                "icon": "🌱",
                "text": "Astuce : Un ordinateur sous Linux peut durer 2 fois plus longtemps qu'avec Windows !",
                "trigger": 4
            },
            {
                "icon": "♻️",
                "text": "Le réemploi du matériel informatique réduit de 80% l'impact environnemental par rapport à l'achat de neuf !",
                "trigger": 6
            },
            {
                "icon": "🎯",
                "text": "Bravo ! Vous progressez dans votre apprentissage de la résistance numérique !",
                "trigger": 8
            }
        ],
        2: [
            {
                "icon": "🔓",
                "text": "Les licences libres permettent de partager, modifier et améliorer les logiciels collectivement !",
                "trigger": 2
            },
            {
                "icon": "🌍",
                "text": "En hébergeant vos données en Europe, vous respectez le RGPD et gardez le contrôle !",
                "trigger": 4
            },
            {
                "icon": "💪",
                "text": "L'autonomie numérique, c'est reprendre le pouvoir sur nos outils et nos données !",
                "trigger": 6
            },
            {
                "icon": "🚀",
                "text": "Excellent ! Vous maîtrisez de mieux en mieux les enjeux du numérique responsable !",
                "trigger": 8
            }
        ],
        3: [
            {
                "icon": "🛡️",
                "text": "Un établissement NIRD, c'est comme le village d'Astérix : résistant et ingénieux !",
                "trigger": 2
            },
            {
                "icon": "🔧",
                "text": "La Forge des communs numériques permet de mutualiser les ressources entre établissements !",
                "trigger": 4
            },
            {
                "icon": "📚",
                "text": "Chaque action NIRD contribue à un numérique plus inclusif, responsable et durable !",
                "trigger": 6
            },
            {
                "icon": "⭐",
                "text": "Impressionnant ! Vous êtes sur la voie pour devenir un expert NIRD !",
                "trigger": 8
            }
        ]
    }
    
    total_tips = 0
    for level, tips in TIPS_DATA.items():
        try:
            quiz = Quiz.objects.get(level=level)
            print(f"\n📝 Quiz Niveau {level}: {quiz.title}")
            
            # Supprimer les anciens tips
            old_count = QuizTip.objects.filter(quiz=quiz).count()
            if old_count > 0:
                QuizTip.objects.filter(quiz=quiz).delete()
                print(f"   🗑️  {old_count} ancien(s) tip(s) supprimé(s)")
            
            # Ajouter les nouveaux tips
            for tip_data in tips:
                QuizTip.objects.create(
                    quiz=quiz,
                    icon=tip_data["icon"],
                    text=tip_data["text"],
                    trigger_question_number=tip_data["trigger"]
                )
                total_tips += 1
                print(f"   ✅ {tip_data['icon']} {tip_data['text'][:40]}...")
            
        except Quiz.DoesNotExist:
            print(f"\n⚠️  Quiz de niveau {level} non trouvé")
        except Exception as e:
            print(f"\n❌ Erreur pour le niveau {level}: {e}")
    
    print(f"\n✨ Total : {total_tips} bulles d'info ajoutées")
    print()

def main():
    """Fonction principale"""
    print("\n" + "═" * 50)
    print("🎯 CONFIGURATION NIRD")
    print("═" * 50)
    print()
    
    # Créer les profils
    create_user_profiles()
    
    # Ajouter les tips
    add_quiz_tips()
    
    print("═" * 50)
    print("🎉 Configuration terminée avec succès !")
    print("═" * 50)
    print()
    print("📋 Prochaines étapes :")
    print("   1. Lancez le serveur : python manage.py runserver")
    print("   2. Ouvrez : http://127.0.0.1:8000/")
    print("   3. Connectez-vous et explorez les nouvelles fonctionnalités !")
    print()
    print("✨ Fonctionnalités disponibles :")
    print("   🎮 Quiz avec bulles d'info fun")
    print("   🏆 Classement avec filtres temporels")
    print("   💬 Réseau social (posts, likes, commentaires)")
    print("   👤 Profils utilisateurs avec statistiques")
    print()
    print("💡 Conseil : Pour générer des utilisateurs de test avec des données :")
    print("   python seed_users.py")
    print()

if __name__ == "__main__":
    main()
