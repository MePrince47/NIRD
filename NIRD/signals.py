from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Quiz, Question, UserQuizAttempt, UserProfile


# Questions par niveau
DEFAULT_QUIZZES = {
   1: [
    {
        "quiz_title": "Niveau 1",
        "text": "Quel est le thème principal du Sujet 2025 de la Nuit de l'Info ?",
        "answers": [
            "Le Village Numérique Résistant",
            "L'Intelligence Artificielle",
            "La Cybersécurité"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 1",
        "text": "Que signifie l'acronyme NIRD ?",
        "answers": [
            "Numérique Inclusif, Responsable et Durable",
            "Nouvelle Infrastructure de Recherche Digitale",
            "National Institute of Research Development"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 1",
        "text": "Qui est le Goliath numérique que les établissements scolaires doivent affronter ?",
        "answers": [
            "L'empire numérique puissant (les Big Tech)",
            "Les petites startups",
            "Les gouvernements locaux"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 1",
        "text": "Nommez l'un des trois piliers qui guident les actions de la démarche NIRD.",
        "answers": [
            "Inclusion, Responsabilité, Durabilité",
            "Innovation, Performance, Expansion",
            "Qualité, Rapidité, Sécurité"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 1",
        "text": "Pourquoi la fin du support de Windows 10 est-elle mentionnée comme un problème ?",
        "answers": [
            "Elle met en évidence la dépendance structurelle aux Big Tech",
            "Elle impose un passage obligatoire à Linux",
            "Elle simplifie la maintenance des ordinateurs"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 1",
        "text": "Quel type de licence est exigé pour la production de l'équipe ?",
        "answers": [
            "Licence libre",
            "Licence propriétaire",
            "Licence commerciale standard"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 1",
        "text": "Quel est l'objectif principal de l'application Web à développer ?",
        "answers": [
            "Aider le public à comprendre comment réduire les dépendances numériques",
            "Vendre des solutions Big Tech",
            "Créer un réseau social éducatif"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 1",
        "text": "Donnez un exemple d'activité de la démarche NIRD liée au matériel.",
        "answers": [
            "Encourager le réemploi et le reconditionnement du matériel",
            "Acheter uniquement du matériel neuf",
            "Centraliser tous les équipements dans un serveur"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 1",
        "text": "Quel est le rôle du logiciel Linux dans la lutte contre l'obsolescence programmée ?",
        "answers": [
            "Promouvoir son usage pour lutter contre l'obsolescence programmée",
            "Remplacer Windows dans toutes les écoles",
            "Créer des systèmes propriétaires"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 1",
        "text": "L'application doit-elle être sérieuse ou proposer une expérience ludique, attractive ou engageante ?",
        "answers": [
            "Elle doit être ludique, attractive ou engageante",
            "Elle doit être uniquement sérieuse et académique",
            "Elle doit suivre un format texte uniquement"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    }
],
    2: [
    {
        "quiz_title": "Niveau 2",
        "text": "Expliquez en quoi les licences coûteuses et les écosystèmes fermés représentent une dépendance aux Big Tech.",
        "answers": [
            "Elles enferment les établissements dans des abonnements et matériels obsolètes",
            "Elles favorisent la liberté numérique",
            "Elles n'ont aucun impact"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 2",
        "text": "Pourquoi est-il important pour le projet NIRD d'utiliser des ressources libres de droit et de mettre la production sous licence libre ?",
        "answers": [
            "Cela favorise un numérique libre, responsable et écocitoyen",
            "Cela complique inutilement le projet",
            "Cela permet de vendre des logiciels propriétaires"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 2",
        "text": "Comment la démarche NIRD encourage-t-elle la sobriété numérique ?",
        "answers": [
            "Elle sensibilise les équipes éducatives et les élèves à la sobriété numérique",
            "Elle impose des règles strictes sur l'utilisation d'Internet",
            "Elle encourage l'achat massif de matériel neuf"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 2",
        "text": "Qu'est-ce que la Forge des communs numériques éducatifs et quel est son rôle dans la mutualisation des ressources ?",
        "answers": [
            "C'est un projet qui mutualise les ressources et outils libres pour NIRD",
            "C'est un logiciel propriétaire",
            "C'est une plateforme de réseaux sociaux pour élèves"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 2",
        "text": "Citez deux types d'acteurs, en dehors des élèves et des enseignants, qui sont associés à la démarche NIRD.",
        "answers": [
            "Directions d'établissements, techniciens et associations partenaires",
            "Banques et entreprises privées",
            "Influenceurs numériques"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 2",
        "text": "Selon le sujet, comment l'École peut-elle devenir un village résistant à l'image du village d'Astérix ?",
        "answers": [
            "En devenant un village résistant, ingénieux, autonome et créatif",
            "En copiant exactement les méthodes des Big Tech",
            "En centralisant toutes les décisions au niveau du ministère"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 2",
        "text": "Quel est l'objectif des équipes en termes d'expérience utilisateur (UX) pour l'application ?",
        "answers": [
            "Donner envie d'apprendre, de comprendre et d'agir",
            "Imposer un parcours strict sans interaction",
            "Créer une interface complexe pour tester les utilisateurs"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 2",
        "text": "Expliquez pourquoi le stockage de données hors UE est perçu comme un risque ou une dépendance.",
        "answers": [
            "Cela contribue à la dépendance aux Big Tech et à la perte de contrôle des données",
            "Cela réduit les coûts pour les établissements",
            "Cela est obligatoire pour tous les logiciels"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 2",
        "text": "En quoi le fait d'adopter des solutions numériques locales et autonomes renforce-t-il le pouvoir d'agir des équipes éducatives ?",
        "answers": [
            "Cela redonne du pouvoir et renforce l'autonomie technologique",
            "Cela empêche toute interaction avec d'autres établissements",
            "Cela oblige à acheter plus de matériel neuf"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 2",
        "text": "Donnez un exemple de format créatif (autre qu'un mini-site narratif) que l'équipe est libre d'utiliser pour son application.",
        "answers": [
            "Outil interactif, parcours visuel, interface gamifiée",
            "Simple document PDF à lire",
            "Une présentation PowerPoint statique"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    }
],

3: [
    {
        "quiz_title": "Niveau 3",
        "text": "Analysez la différence d'approche entre une initiative d'en bas et les directives venant des services académiques ou du ministère.",
        "answers": [
            "Initiative d'en bas montre aux services supérieurs l'urgence d'agir",
            "Les directives supérieures imposent des solutions sans retour",
            "Il n'y a pas de différence"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 3",
        "text": "Discutez de l'équilibre à trouver entre rendre l'application ludique et attractive et transmettre l'esprit de résistance numérique propre à NIRD.",
        "answers": [
            "L'application doit être ludique et engageante tout en transmettant l'esprit de résistance",
            "L'application doit être sérieuse uniquement",
            "L'important est l'esthétique, pas le contenu"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 3",
        "text": "Comment la promotion de l'usage de Linux par NIRD permet-elle de lutter contre l'obsolescence programmée et de réduire les coûts de licence ?",
        "answers": [
            "Linux permet de faire fonctionner du matériel ancien et est libre de licence",
            "Linux impose des licences coûteuses",
            "Linux ne peut pas remplacer Windows 10"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 3",
        "text": "Quelles stratégies de gamification pourraient être utilisées pour faire comprendre la transition vers un numérique plus durable ?",
        "answers": [
            "Interactivité, énigmes, défis, scénarios et illustrations",
            "Simple texte à lire",
            "Présentations statiques sans interaction"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 3",
        "text": "Élaborez sur la manière dont la démarche NIRD répond aux enjeux d'un numérique à la fois Inclusif et Durable.",
        "answers": [
            "Elle permet le réemploi, réduit les coûts et rend le numérique accessible",
            "Elle favorise uniquement la durabilité",
            "Elle ne s'intéresse qu'à l'inclusion sociale"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 3",
        "text": "Quel rôle les Collectivités territoriales peuvent-elles jouer pour aider un établissement à réduire ses dépendances numériques ?",
        "answers": [
            "Soutenir le financement du reconditionnement et des solutions libres",
            "Acheter uniquement du matériel neuf",
            "Aucune implication n'est nécessaire"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 3",
        "text": "Dans l'objectif de faire croître la communauté NIRD, quelles fonctionnalités concrètes l'application pourrait-elle inclure ?",
        "answers": [
            "Permettre contribution, animation et valorisation des solutions proposées",
            "Limiter la participation aux seuls enseignants",
            "Partager uniquement des fichiers PDF"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 3",
        "text": "Décrivez comment le concept du réemploi et du reconditionnement du matériel s'oppose au modèle économique des Big Tech.",
        "answers": [
            "Le réemploi utilise le matériel existant et lutte contre l'obsolescence programmée",
            "Il favorise l'achat continu de matériel neuf",
            "Il centralise toutes les données sur un serveur unique"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 3",
        "text": "Quels sont les risques ou défis techniques liés à développer une application sous licence libre ?",
        "answers": [
            "Assurer que toutes les ressources utilisées sont libres et compatibles avec la licence",
            "Aucun risque, tout est libre automatiquement",
            "Limiter l'utilisation de Linux uniquement"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    },
    {
        "quiz_title": "Niveau 3",
        "text": "Pourquoi l'autonomie technologique est-elle un enjeu de souveraineté numérique pour l'éducation ?",
        "answers": [
            "Renforcer l'autonomie permet de reprendre le contrôle des outils et données éducatives",
            "Elle permet uniquement de suivre les directives ministérielles",
            "Elle n'a pas d'impact sur la souveraineté numérique"
        ],
        "correct_index": 0,
        "points": 1,
        "time_limit": 30
    }
],

}


@receiver(post_migrate)
def create_default_quizzes(sender, **kwargs):
    """
    Signal qui crée automatiquement les quiz et questions de base
    après chaque migration.
    """
    for level, questions in DEFAULT_QUIZZES.items():
        for q in questions:
            quiz, created = Quiz.objects.get_or_create(
                title=q["quiz_title"],
                level=level
            )
            # Vérifie si la question existe déjà
            if not Question.objects.filter(quiz=quiz, text=q["text"]).exists():
                Question.objects.create(
                    quiz=quiz,
                    text=q["text"],
                    answers=q["answers"],
                    correct_index=q["correct_index"],
                    points=q.get("points", 1),
                    time_limit=q.get("time_limit", 30)
                )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un profil pour chaque nouvel utilisateur"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarde le profil utilisateur"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(post_save, sender=UserQuizAttempt)
def update_user_stats_on_quiz_complete(sender, instance, **kwargs):
    """Met à jour les statistiques de l'utilisateur après un quiz"""
    if instance.completed:
        profile, created = UserProfile.objects.get_or_create(user=instance.user)
        profile.update_stats()
