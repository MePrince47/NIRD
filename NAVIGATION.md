# 🧭 Navigation de la plateforme NIRD

## Pages principales accessibles

### 🏠 Accueil / Quiz
**URL:** `http://127.0.0.1:8000/`

Page d'accueil avec la liste de tous les quiz disponibles organisés par niveau.
- Accessible depuis n'importe quelle page via le bouton "🏠 Quiz" dans le header

### 🏆 Classement
**URL:** `http://127.0.0.1:8000/leaderboard/`

Tableau de classement des meilleurs joueurs avec filtres par période.
- Accessible via le bouton "🏆 Classement" dans le header

### 💬 Communauté / Fil Social
**URL:** `http://127.0.0.1:8000/social/`

Fil d'actualité social où les utilisateurs peuvent :
- Publier des posts
- Liker les posts des autres
- Commenter les publications
- Partager leurs réussites aux quiz

Accessible via le bouton "💬 Communauté" dans le header

### 👤 Profil Utilisateur
**URL:** `http://127.0.0.1:8000/profile/<username>/`

Page de profil personnel affichant :
- Avatar et informations utilisateur
- Niveau et points totaux
- Statistiques de quiz
- Historique des quiz complétés
- Posts récents de l'utilisateur

Accessible via :
- Le bouton "👤 Profil" dans le header (sur certaines pages)
- En cliquant sur un nom d'utilisateur dans le fil social ou le classement

### 📝 Question de Quiz
**URL:** `http://127.0.0.1:8000/quiz/<quiz_id>/question/`

Page de question interactive avec :
- Timer
- Choix multiples
- Navigation complète dans le header

### 📊 Résultats
**URL:** `http://127.0.0.1:8000/attempt/<attempt_id>/result/`

Page de résultats après avoir complété un quiz avec :
- Score obtenu
- Détails de chaque réponse (correcte/incorrecte)
- Bonnes réponses pour les questions manquées
- Statistiques personnelles
- Boutons d'action pour naviguer vers :
  - 🏠 Retour aux quiz
  - 🏆 Classement
  - 💬 Fil social
  - 👤 Mon profil

## Navigation cohérente

Toutes les pages principales incluent un **header unifié** avec :
- Logo NIRD
- Menu de navigation (Quiz, Classement, Communauté)
- Informations utilisateur (avatar, nom, niveau)
- Bouton de profil ou déconnexion

## Comptes de test

Pour tester la plateforme, utilisez l'un de ces comptes :

```
Username: alice_nird, bob_tech, charlie_eco, diana_code, ethan_libre, fiona_green, gabriel_dev, hannah_edu
Password: nird2025
```

## Démarrage rapide

1. Lancer le serveur :
   ```bash
   python manage.py runserver
   ```

2. Ouvrir le navigateur :
   ```
   http://127.0.0.1:8000/
   ```

3. Se connecter avec un compte de test

4. Explorer la plateforme via la navigation !
