#!/usr/bin/env python
"""
Script pour ajouter des bulles d'info fun aux quiz NIRD
Ces tips apparaissent pendant le quiz pour aider et encourager les joueurs
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nird_Quiz.settings')
django.setup()

from NIRD.models import Quiz, QuizTip

# Tips fun pour les différents niveaux de quiz
TIPS_DATA = {
    1: [  # Niveau 1
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
    2: [  # Niveau 2
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
    3: [  # Niveau 3
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

def add_quiz_tips():
    """Ajoute les tips aux quiz existants"""
    print("🎯 Ajout des bulles d'info fun aux quiz NIRD...\n")
    
    for level, tips in TIPS_DATA.items():
        try:
            quiz = Quiz.objects.get(level=level)
            print(f"📝 Traitement du quiz Niveau {level}: {quiz.title}")
            
            # Supprimer les anciens tips pour ce quiz
            QuizTip.objects.filter(quiz=quiz).delete()
            
            # Ajouter les nouveaux tips
            for tip_data in tips:
                tip = QuizTip.objects.create(
                    quiz=quiz,
                    icon=tip_data["icon"],
                    text=tip_data["text"],
                    trigger_question_number=tip_data["trigger"]
                )
                print(f"  ✅ Ajouté: {tip.icon} {tip.text[:50]}...")
            
            print(f"  ✨ {len(tips)} tips ajoutés pour le niveau {level}\n")
            
        except Quiz.DoesNotExist:
            print(f"  ⚠️  Quiz de niveau {level} non trouvé\n")
        except Exception as e:
            print(f"  ❌ Erreur pour le niveau {level}: {e}\n")
    
    print("🎉 Terminé ! Les bulles d'info ont été ajoutées aux quiz.")
    print("💬 Les joueurs verront maintenant des conseils fun pendant leurs quiz !")

if __name__ == "__main__":
    add_quiz_tips()
