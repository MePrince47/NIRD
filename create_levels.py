#!/usr/bin/env python
"""
Script pour créer plusieurs niveaux de quiz NIRD
NIRD = Numérique Inclusif, Responsable et Durable
Thème : Résistance numérique des établissements scolaires face aux Big Tech
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nird_Quiz.settings')
django.setup()

from NIRD.models import Quiz, Question

def create_quiz_levels():
    """Crée 6 niveaux de quiz avec des questions d'exemple"""
    
    # Supprimer les quiz existants (optionnel)
    # Quiz.objects.all().delete()
    
    quiz_data = [
        {
            'level': 1,
            'title': 'Découverte de NIRD',
            'questions': [
                {
                    'text': 'Que signifie l\'acronyme NIRD ?',
                    'answers': [
                        'Numérique Inclusif, Responsable et Durable',
                        'Nouvelles Innovations en Réseaux Digitaux',
                        'Normes Informatiques et Règles Digitales',
                        'Navigation Internet et Ressources Digitales'
                    ],
                    'correct_index': 0,
                    'points': 10,
                    'time_limit': 30
                },
                {
                    'text': 'Quel est le principal problème posé par la fin du support de Windows 10 ?',
                    'answers': [
                        'Les ordinateurs deviennent plus lents',
                        'Du matériel fonctionnel devient obsolète',
                        'Les écrans ne fonctionnent plus',
                        'Internet ne marche plus'
                    ],
                    'correct_index': 1,
                    'points': 15,
                    'time_limit': 40
                },
                {
                    'text': 'À quelle célèbre BD est comparée la démarche NIRD dans sa résistance ?',
                    'answers': [
                        'Tintin',
                        'Lucky Luke',
                        'Astérix',
                        'Spirou'
                    ],
                    'correct_index': 2,
                    'points': 10,
                    'time_limit': 30
                },
                {
                    'text': 'Où est né le projet NIRD ?',
                    'answers': [
                        'Au lycée Carnot de Bruay-la-Buissière',
                        'À Paris',
                        'À Lyon',
                        'À Marseille'
                    ],
                    'correct_index': 0,
                    'points': 10,
                    'time_limit': 30
                },
            ]
        },
        {
            'level': 2,
            'title': 'Logiciels Libres et Alternatives',
            'questions': [
                {
                    'text': 'Quel système d\'exploitation libre est promu par NIRD pour lutter contre l\'obsolescence ?',
                    'answers': [
                        'Windows',
                        'macOS',
                        'Linux',
                        'ChromeOS'
                    ],
                    'correct_index': 2,
                    'points': 15,
                    'time_limit': 30
                },
                {
                    'text': 'Que signifie le "I" dans NIRD ?',
                    'answers': [
                        'Informatique',
                        'Inclusif',
                        'Innovation',
                        'International'
                    ],
                    'correct_index': 1,
                    'points': 10,
                    'time_limit': 30
                },
                {
                    'text': 'Quel est l\'avantage principal des logiciels libres pour les établissements ?',
                    'answers': [
                        'Ils sont plus jolis',
                        'Ils réduisent les coûts et la dépendance aux éditeurs',
                        'Ils sont plus lents',
                        'Ils nécessitent plus de formations'
                    ],
                    'correct_index': 1,
                    'points': 20,
                    'time_limit': 45
                },
                {
                    'text': 'Qu\'est-ce que la Forge des communs numériques éducatifs ?',
                    'answers': [
                        'Un magasin de logiciels',
                        'Une plateforme de partage de ressources libres',
                        'Un réseau social',
                        'Un jeu vidéo'
                    ],
                    'correct_index': 1,
                    'points': 15,
                    'time_limit': 40
                },
            ]
        },
        {
            'level': 3,
            'title': 'Numérique Responsable',
            'questions': [
                {
                    'text': 'Que signifie le "R" dans NIRD ?',
                    'answers': [
                        'Rapide',
                        'Responsable',
                        'Rentable',
                        'Révolutionnaire'
                    ],
                    'correct_index': 1,
                    'points': 10,
                    'time_limit': 30
                },
                {
                    'text': 'Pourquoi la protection des données personnelles est-elle importante dans NIRD ?',
                    'answers': [
                        'Pour respecter la vie privée et éviter le stockage hors UE',
                        'Pour rendre les ordinateurs plus rapides',
                        'Pour économiser de l\'électricité',
                        'Pour avoir de meilleures notes'
                    ],
                    'correct_index': 0,
                    'points': 20,
                    'time_limit': 45
                },
                {
                    'text': 'Quel est un problème majeur des écosystèmes fermés (comme ceux des Big Tech) ?',
                    'answers': [
                        'Ils sont gratuits',
                        'Ils créent une dépendance et limitent l\'autonomie',
                        'Ils sont trop simples',
                        'Ils consomment peu d\'énergie'
                    ],
                    'correct_index': 1,
                    'points': 25,
                    'time_limit': 50
                },
                {
                    'text': 'Que permet la mutualisation des ressources libres ?',
                    'answers': [
                        'De payer plus cher',
                        'De partager et co-construire des solutions',
                        'D\'isoler les établissements',
                        'De compliquer les choses'
                    ],
                    'correct_index': 1,
                    'points': 20,
                    'time_limit': 45
                },
            ]
        },
        {
            'level': 4,
            'title': 'Numérique Durable',
            'questions': [
                {
                    'text': 'Que signifie le "D" dans NIRD ?',
                    'answers': [
                        'Digital',
                        'Durable',
                        'Dynamique',
                        'Diversifié'
                    ],
                    'correct_index': 1,
                    'points': 10,
                    'time_limit': 30
                },
                {
                    'text': 'Qu\'est-ce que l\'obsolescence programmée ?',
                    'answers': [
                        'Un programme informatique',
                        'La stratégie de rendre volontairement du matériel obsolète',
                        'Un cours de programmation',
                        'Une mise à jour automatique'
                    ],
                    'correct_index': 1,
                    'points': 20,
                    'time_limit': 45
                },
                {
                    'text': 'Comment NIRD favorise-t-il la durabilité du matériel ?',
                    'answers': [
                        'En achetant du matériel neuf chaque année',
                        'En promouvant le réemploi et le reconditionnement',
                        'En jetant les vieux ordinateurs',
                        'En utilisant uniquement des tablettes'
                    ],
                    'correct_index': 1,
                    'points': 25,
                    'time_limit': 50
                },
                {
                    'text': 'Quel est l\'impact de la sobriété numérique ?',
                    'answers': [
                        'Augmenter la consommation d\'énergie',
                        'Réduire l\'empreinte écologique du numérique',
                        'Ralentir les ordinateurs',
                        'Supprimer Internet'
                    ],
                    'correct_index': 1,
                    'points': 25,
                    'time_limit': 50
                },
            ]
        },
        {
            'level': 5,
            'title': 'Transition NIRD en Action',
            'questions': [
                {
                    'text': 'Quels sont les trois piliers de la démarche NIRD ?',
                    'answers': [
                        'Inclusion, Responsabilité, Durabilité',
                        'Innovation, Rapidité, Diversité',
                        'Internet, Réseaux, Données',
                        'Installation, Réparation, Développement'
                    ],
                    'correct_index': 0,
                    'points': 25,
                    'time_limit': 45
                },
                {
                    'text': 'Qui sont les acteurs impliqués dans la démarche NIRD ?',
                    'answers': [
                        'Uniquement les enseignants',
                        'Élèves, enseignants, directions, techniciens, collectivités',
                        'Seulement les informaticiens',
                        'Uniquement le ministère'
                    ],
                    'correct_index': 1,
                    'points': 30,
                    'time_limit': 50
                },
                {
                    'text': 'Comment un établissement peut-il commencer sa transition NIRD ?',
                    'answers': [
                        'Tout changer d\'un coup',
                        'De manière progressive et réaliste',
                        'Attendre que tout le monde soit d\'accord',
                        'Abandonner tout le numérique'
                    ],
                    'correct_index': 1,
                    'points': 30,
                    'time_limit': 60
                },
                {
                    'text': 'Quel rôle jouent les éco-délégués dans NIRD ?',
                    'answers': [
                        'Aucun rôle',
                        'Sensibiliser et promouvoir la sobriété numérique',
                        'Réparer les ordinateurs',
                        'Acheter du matériel'
                    ],
                    'correct_index': 1,
                    'points': 25,
                    'time_limit': 45
                },
            ]
        },
        {
            'level': 6,
            'title': 'Expert NIRD',
            'questions': [
                {
                    'text': 'Quel est l\'objectif ultime de la démarche NIRD ?',
                    'answers': [
                        'Économiser de l\'argent uniquement',
                        'Construire un numérique éducatif autonome, durable et éthique',
                        'Utiliser uniquement des ordinateurs anciens',
                        'Supprimer tous les logiciels propriétaires'
                    ],
                    'correct_index': 1,
                    'points': 35,
                    'time_limit': 60
                },
                {
                    'text': 'Pourquoi NIRD est-il comparé au village d\'Astérix ?',
                    'answers': [
                        'Parce qu\'il résiste à l\'empire des Big Tech',
                        'Parce qu\'il est petit',
                        'Parce qu\'il est en Gaule',
                        'Parce qu\'il utilise de la potion magique'
                    ],
                    'correct_index': 0,
                    'points': 30,
                    'time_limit': 50
                },
                {
                    'text': 'Quel est le rôle de la Direction du numérique pour l\'éducation dans NIRD ?',
                    'answers': [
                        'Elle n\'a aucun rôle',
                        'Elle soutient le projet et la Forge des communs numériques',
                        'Elle impose NIRD à tous',
                        'Elle vend des logiciels'
                    ],
                    'correct_index': 1,
                    'points': 30,
                    'time_limit': 50
                },
                {
                    'text': 'Comment NIRD favorise-t-il l\'autonomie technologique des établissements ?',
                    'answers': [
                        'En les rendant dépendants d\'un nouveau système',
                        'En leur donnant le pouvoir d\'agir et de choisir leurs outils',
                        'En imposant des solutions uniques',
                        'En supprimant la technologie'
                    ],
                    'correct_index': 1,
                    'points': 40,
                    'time_limit': 60
                },
            ]
        },
    ]
    
    for quiz_info in quiz_data:
        # Créer ou récupérer le quiz
        quiz, created = Quiz.objects.get_or_create(
            level=quiz_info['level'],
            defaults={'title': quiz_info['title']}
        )
        
        if created:
            print(f"✅ Quiz créé : {quiz.title} (Niveau {quiz.level})")
            
            # Créer les questions
            for idx, q_data in enumerate(quiz_info['questions'], start=1):
                Question.objects.create(
                    quiz=quiz,
                    text=q_data['text'],
                    answers=q_data['answers'],
                    correct_index=q_data['correct_index'],
                    order=idx,
                    points=q_data['points'],
                    time_limit=q_data['time_limit']
                )
            print(f"   📝 {len(quiz_info['questions'])} questions ajoutées")
        else:
            print(f"ℹ️  Quiz déjà existant : {quiz.title} (Niveau {quiz.level})")
    
    print("\n🎉 Tous les niveaux ont été créés avec succès !")
    print(f"📊 Total : {Quiz.objects.count()} quiz avec {Question.objects.count()} questions")

if __name__ == '__main__':
    create_quiz_levels()
