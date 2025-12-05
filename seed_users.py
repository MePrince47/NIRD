#!/usr/bin/env python
"""
Script de seeding pour créer des utilisateurs de test avec leurs données
Génère des utilisateurs, profils, quiz complétés, posts, likes et commentaires
"""

import os
import django
import random
from datetime import datetime, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nird_Quiz.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from NIRD.models import (
    Quiz, Question, UserQuizAttempt, UserAnswer,
    UserProfile, Post, Comment, Like
)

# Données pour les utilisateurs de test
USERS_DATA = [
    {
        "username": "alice_nird",
        "email": "alice@nird.fr",
        "first_name": "Alice",
        "last_name": "Dupont",
        "avatar": "🦊",
        "bio": "Passionnée par le numérique responsable et Linux !"
    },
    {
        "username": "bob_tech",
        "email": "bob@nird.fr",
        "first_name": "Bob",
        "last_name": "Martin",
        "avatar": "🐼",
        "bio": "Enseignant en informatique, militant pour le logiciel libre"
    },
    {
        "username": "charlie_eco",
        "email": "charlie@nird.fr",
        "first_name": "Charlie",
        "last_name": "Dubois",
        "avatar": "🌱",
        "bio": "Défenseur de l'écologie numérique et du réemploi"
    },
    {
        "username": "diana_code",
        "email": "diana@nird.fr",
        "first_name": "Diana",
        "last_name": "Leroy",
        "avatar": "💻",
        "bio": "Développeuse passionnée par les communs numériques"
    },
    {
        "username": "ethan_libre",
        "email": "ethan@nird.fr",
        "first_name": "Ethan",
        "last_name": "Bernard",
        "avatar": "🚀",
        "bio": "Étudiant engagé pour un numérique plus libre"
    },
    {
        "username": "fiona_green",
        "email": "fiona@nird.fr",
        "first_name": "Fiona",
        "last_name": "Petit",
        "avatar": "🌍",
        "bio": "Militante pour la sobriété numérique"
    },
    {
        "username": "gabriel_dev",
        "email": "gabriel@nird.fr",
        "first_name": "Gabriel",
        "last_name": "Roux",
        "avatar": "⚡",
        "bio": "Dev full-stack, fan de solutions open source"
    },
    {
        "username": "hannah_edu",
        "email": "hannah@nird.fr",
        "first_name": "Hannah",
        "last_name": "Moreau",
        "avatar": "📚",
        "bio": "Enseignante, promotrice de l'éducation numérique responsable"
    }
]

# Posts d'exemple
SAMPLE_POSTS = [
    "Je viens de découvrir que Linux peut prolonger la vie de mon ancien PC de 5 ans ! C'est incroyable 🚀",
    "Qui utilise déjà des logiciels libres dans son établissement ? Partagez vos expériences !",
    "La sobriété numérique commence par de petits gestes : éteindre son PC, limiter les emails, utiliser du matériel reconditionné... 🌱",
    "J'ai complété tous les quiz NIRD ! Les conseils sur l'autonomie numérique sont vraiment utiles 💡",
    "Le réemploi du matériel informatique devrait être la norme dans toutes les écoles 🔄",
    "Quelqu'un a des retours d'expérience sur la migration vers Linux dans l'éducation ?",
    "Les Big Tech nous rendent dépendants... Il est temps de reprendre le contrôle ! 💪",
    "La Forge des communs numériques est une ressource fantastique pour mutualiser nos outils 🛠️",
    "Bravo à l'équipe NIRD pour cette plateforme ! C'est exactement ce dont nous avions besoin 🎯",
    "Le RGPD et l'hébergement en Europe : un enjeu crucial pour nos données éducatives 🔒",
    "J'ai installé Linux sur 10 vieux PC de l'école, ils fonctionnent comme neufs ! ♻️",
    "Les licences libres permettent vraiment de partager et d'améliorer collectivement nos outils 🤝",
    "Qui participe à la Nuit de l'Info cette année ? On peut échanger sur nos projets NIRD ! 🌙",
    "L'obsolescence programmée est un fléau... Luttons avec le logiciel libre ! ⚔️",
    "Les élèves adorent les quiz interactifs ! Gamification + éducation = succès 🎮"
]

# Commentaires d'exemple
SAMPLE_COMMENTS = [
    "Excellente initiative ! 👍",
    "Je suis totalement d'accord avec toi !",
    "Merci pour le partage, très intéressant 💡",
    "J'ai eu la même expérience dans mon établissement",
    "Super idée, je vais tester ça !",
    "C'est exactement ce que je cherchais 🎯",
    "Bravo pour ton engagement ! 💪",
    "On devrait tous suivre cet exemple",
    "Merci pour ces conseils pratiques !",
    "Je partage complètement cette vision 🌱",
    "Génial ! Continue comme ça 🚀",
    "Très bon point, je n'y avais pas pensé",
    "C'est inspirant ! 😊",
    "On a besoin de plus de personnes comme toi",
    "Merci pour cette contribution à la communauté NIRD ❤️"
]

def create_users():
    """Crée les utilisateurs de test avec leurs profils"""
    print("👥 Création des utilisateurs de test...")
    print("─" * 60)
    
    created_users = []
    
    for user_data in USERS_DATA:
        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=user_data["username"]).exists():
            print(f"⚠️  {user_data['username']} existe déjà, ignoré")
            user = User.objects.get(username=user_data["username"])
            created_users.append(user)
            continue
        
        # Créer l'utilisateur
        user = User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password="nird2025",  # Mot de passe par défaut
            first_name=user_data["first_name"],
            last_name=user_data["last_name"]
        )
        
        # Mettre à jour le profil (créé automatiquement par les signaux)
        profile = user.profile
        profile.avatar_emoji = user_data["avatar"]
        profile.bio = user_data["bio"]
        profile.save()
        
        created_users.append(user)
        print(f"✅ {user_data['avatar']} {user_data['username']} créé")
    
    print(f"\n✨ {len(created_users)} utilisateurs prêts\n")
    return created_users

def simulate_quiz_attempts(users):
    """Simule des tentatives de quiz pour les utilisateurs"""
    print("🎮 Simulation des quiz complétés...")
    print("─" * 60)
    
    quizzes = list(Quiz.objects.all())
    if not quizzes:
        print("⚠️  Aucun quiz disponible, ignoré\n")
        return
    
    total_attempts = 0
    
    for user in users:
        # Chaque utilisateur complète entre 1 et 5 quiz
        num_quizzes = random.randint(1, min(5, len(quizzes)))
        selected_quizzes = random.sample(quizzes, num_quizzes)
        
        for quiz in selected_quizzes:
            # Vérifier si l'utilisateur a déjà fait ce quiz
            if UserQuizAttempt.objects.filter(user=user, quiz=quiz, completed=True).exists():
                continue
            
            # Créer une tentative
            attempt = UserQuizAttempt.objects.create(
                user=user,
                quiz=quiz,
                completed=True
            )
            
            # Simuler les réponses
            questions = list(quiz.questions.all())
            correct_count = 0
            
            for question in questions:
                # 70% de chance de répondre correctement
                is_correct = random.random() < 0.7
                selected_index = question.correct_index if is_correct else random.randint(0, len(question.answers) - 1)
                
                UserAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_index=selected_index,
                    correct=is_correct,
                    created_at=timezone.now() - timedelta(days=random.randint(0, 30))
                )
                
                if is_correct:
                    correct_count += question.points
            
            attempt.score = correct_count
            attempt.save()
            total_attempts += 1
        
        # Mettre à jour les stats du profil
        user.profile.update_stats()
        print(f"✅ {user.profile.avatar_emoji} {user.username}: {num_quizzes} quiz, niveau {user.profile.level}")
    
    print(f"\n✨ {total_attempts} quiz complétés au total\n")

def create_posts(users):
    """Crée des posts pour les utilisateurs"""
    print("💬 Création des posts...")
    print("─" * 60)
    
    quizzes = list(Quiz.objects.all())
    created_posts = []
    
    for user in users:
        # Chaque utilisateur crée entre 1 et 3 posts
        num_posts = random.randint(1, 3)
        
        for _ in range(num_posts):
            content = random.choice(SAMPLE_POSTS)
            
            # 30% de chance de lier à un quiz
            related_quiz = random.choice(quizzes) if quizzes and random.random() < 0.3 else None
            
            # Date aléatoire dans les 30 derniers jours
            created_at = timezone.now() - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            post = Post.objects.create(
                author=user,
                content=content,
                related_quiz=related_quiz,
                created_at=created_at
            )
            
            created_posts.append(post)
        
        print(f"✅ {user.profile.avatar_emoji} {user.username}: {num_posts} post(s)")
    
    print(f"\n✨ {len(created_posts)} posts créés\n")
    return created_posts

def create_interactions(users, posts):
    """Crée des likes et commentaires"""
    print("❤️ Création des interactions (likes et commentaires)...")
    print("─" * 60)
    
    total_likes = 0
    total_comments = 0
    
    for post in posts:
        # Likes : entre 0 et 8 utilisateurs aiment chaque post
        available_likers = [u for u in users if u != post.author]
        num_likes = random.randint(0, min(8, len(available_likers)))
        likers = random.sample(available_likers, num_likes)
        
        for liker in likers:
            Like.objects.get_or_create(user=liker, post=post)
            total_likes += 1
        
        # Commentaires : entre 0 et 5 commentaires par post
        available_commenters = [u for u in users if u != post.author]
        num_comments = random.randint(0, min(5, len(available_commenters)))
        commenters = random.sample(available_commenters, num_comments)
        
        for commenter in commenters:
            content = random.choice(SAMPLE_COMMENTS)
            
            Comment.objects.create(
                post=post,
                author=commenter,
                content=content,
                created_at=post.created_at + timedelta(hours=random.randint(1, 48))
            )
            total_comments += 1
    
    print(f"✅ {total_likes} likes créés")
    print(f"✅ {total_comments} commentaires créés")
    print()

def display_summary(users):
    """Affiche un résumé des données créées"""
    print("=" * 60)
    print("📊 RÉSUMÉ DES DONNÉES CRÉÉES")
    print("=" * 60)
    print()
    
    print("👥 Utilisateurs créés :")
    for user in users:
        profile = user.profile
        attempts = UserQuizAttempt.objects.filter(user=user, completed=True).count()
        posts = Post.objects.filter(author=user).count()
        
        print(f"   {profile.avatar_emoji} {user.username:15} | Niveau {profile.level} | {profile.total_points:3} pts | {attempts} quiz | {posts} posts")
    
    print()
    print(f"📊 Statistiques globales :")
    print(f"   • {User.objects.count()} utilisateurs au total")
    print(f"   • {Post.objects.count()} posts")
    print(f"   • {Comment.objects.count()} commentaires")
    print(f"   • {Like.objects.count()} likes")
    print(f"   • {UserQuizAttempt.objects.filter(completed=True).count()} quiz complétés")
    print()

def main():
    """Fonction principale"""
    print("\n" + "=" * 60)
    print("🌱 SEEDING DE LA BASE DE DONNÉES NIRD")
    print("=" * 60)
    print()
    
    # 1. Créer les utilisateurs
    users = create_users()
    
    # 2. Simuler des quiz
    simulate_quiz_attempts(users)
    
    # 3. Créer des posts
    posts = create_posts(users)
    
    # 4. Créer des interactions
    create_interactions(users, posts)
    
    # 5. Afficher le résumé
    display_summary(users)
    
    print("=" * 60)
    print("🎉 SEEDING TERMINÉ AVEC SUCCÈS !")
    print("=" * 60)
    print()
    print("📋 Informations de connexion :")
    print("   Username : alice_nird (ou bob_tech, charlie_eco, etc.)")
    print("   Password : nird2025")
    print()
    print("🚀 Lancez le serveur :")
    print("   python manage.py runserver")
    print()
    print("🌐 Puis ouvrez : http://127.0.0.1:8000/")
    print()

if __name__ == "__main__":
    main()
