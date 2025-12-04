# NIRD Quiz 🛡️

**Le Village Numérique Résistant : Comment les établissements scolaires peuvent tenir tête aux Big Tech ?**

Une application web ludique et pédagogique développée pour la **Nuit de l'Info 2025**, permettant de découvrir et comprendre la démarche **NIRD** (Numérique Inclusif, Responsable et Durable) à travers un parcours de quiz progressif.

## 🎯 Mission

Face à l'empire numérique des Big Tech (matériel obsolète, licences coûteuses, données hors UE, écosystèmes fermés...), l'École peut devenir un village résistant, à l'image d'Astérix. Cette application aide élèves, enseignants, familles et collectivités à comprendre comment réduire leurs dépendances numériques.

## 📋 Fonctionnalités

- **Parcours de résistance numérique** : 6 niveaux progressifs pour découvrir NIRD
- **Explication interactive** : Présentation des 4 piliers NIRD (Numérique libre, Inclusif, Responsable, Durable)
- **Quiz pédagogiques** : Questions sur l'obsolescence programmée, les logiciels libres, la sobriété numérique
- **Authentification utilisateur** : Suivi personnalisé de la progression
- **Interface gamifiée** : Design moderne style Kiro Game avec badges et niveaux
- **Système de points** : Évaluation des connaissances acquises
- **Responsive design** : Accessible sur tous les appareils

## 🛠️ Technologies utilisées

- **Framework** : Django 4.2.20
- **Base de données** : SQLite3
- **Backend** : Python 3.x
- **Frontend** : HTML/CSS/JavaScript

## 📁 Structure du projet

```
NIRD/
├── NIRD/                   # Application principale
│   ├── models.py          # Modèles (Quiz, Question, UserQuizAttempt, UserAnswer)
│   ├── views.py           # Vues et logique métier
│   ├── urls.py            # Routes de l'application
│   ├── admin.py           # Configuration de l'interface d'administration
│   └── signals.py         # Signaux Django
├── Nird_Quiz/             # Configuration du projet
│   ├── settings.py        # Paramètres Django
│   ├── urls.py            # Routes principales
│   └── wsgi.py            # Configuration WSGI
├── templates/             # Templates HTML
│   └── NIRD/
│       ├── home.html      # Page d'accueil avec liste des quiz
│       ├── login.html     # Page de connexion
│       ├── question.html  # Affichage des questions
│       └── result.html    # Page de résultats
├── static/                # Fichiers statiques (CSS, JS)
├── db.sqlite3            # Base de données
└── manage.py             # Script de gestion Django
```

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/MePrince47/NIRD.git
cd NIRD
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install django==4.2.20
```

4. **Appliquer les migrations**
```bash
python manage.py migrate
```

5. **Créer un superutilisateur (optionnel)**
```bash
python manage.py createsuperuser
```

6. **Collecter les fichiers statiques**
```bash
python manage.py collectstatic --noinput
```

7. **Créer les niveaux de quiz**
```bash
python create_levels.py
```
Ce script créera automatiquement 6 niveaux de quiz avec des questions sur :
- Niveau 1 : Découverte de NIRD
- Niveau 2 : Logiciels Libres et Alternatives
- Niveau 3 : Numérique Responsable
- Niveau 4 : Numérique Durable
- Niveau 5 : Transition NIRD en Action
- Niveau 6 : Expert NIRD

## 🎮 Utilisation

### Démarrer le serveur de développement

```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : `http://127.0.0.1:8000/`

### Accéder à l'interface d'administration

Rendez-vous sur `http://127.0.0.1:8000/admin/` pour gérer les quiz, questions et utilisateurs.

## 🌟 Les 4 Piliers de NIRD

### N - Numérique
Un numérique **libre et ouvert**, basé sur les logiciels libres et les communs numériques éducatifs.

### I - Inclusif
**Accessible à tous**, sans discrimination, favorisant l'autonomie et la participation de tous les acteurs.

### R - Responsable
**Éthique et respectueux** des données personnelles et de la vie privée, évitant le stockage hors UE.

### D - Durable
**Sobre et écologique**, luttant contre l'obsolescence programmée et favorisant le réemploi du matériel.

## 📊 Modèles de données

### Quiz
- `title` : Titre du quiz (ex: "Découverte de NIRD")
- `level` : Niveau de progression (1 à 6)

### Question
- `quiz` : Référence au quiz parent
- `text` : Texte de la question
- `answers` : Liste des réponses possibles (JSON)
- `correct_index` : Index de la réponse correcte
- `order` : Ordre d'affichage
- `points` : Points attribués
- `time_limit` : Temps limite en secondes

### UserQuizAttempt
- `user` : Utilisateur
- `quiz` : Quiz concerné
- `score` : Score obtenu
- `completed` : Statut de complétion

### UserAnswer
- `attempt` : Tentative associée
- `question` : Question concernée
- `selected_index` : Réponse sélectionnée
- `correct` : Indicateur de réponse correcte

## 🔧 Configuration

### Paramètres importants dans `settings.py`

- `DEBUG = True` : Mode développement (à désactiver en production)
- `ALLOWED_HOSTS = []` : À configurer pour la production
- `SECRET_KEY` : À remplacer par une clé secrète unique en production
- `DATABASES` : Configuration SQLite par défaut

## 🔐 Sécurité

⚠️ **Avant le déploiement en production** :
- Changez la `SECRET_KEY`
- Définissez `DEBUG = False`
- Configurez `ALLOWED_HOSTS`
- Utilisez une base de données plus robuste (PostgreSQL, MySQL)
- Configurez HTTPS
- Activez les mesures de sécurité Django recommandées

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 🔗 Ressources NIRD

### Site officiel et documentation
- **Site NIRD** : [https://nird.forge.apps.education.fr/](https://nird.forge.apps.education.fr/)
- **Forge des communs numériques éducatifs** : Plateforme de partage de ressources libres

### Médias et reportages
- [Windows 11 : l'alternative des logiciels libres](https://video.echirolles.fr/w/hVykGUtRZqRen6eiutqRvQ) (France 3 Alpes, 2 min)
- [Mises à jour Windows : le logiciel libre comme solution ?](https://www.radiofrance.fr/franceinter/podcasts/le-grand-reportage-de-france-inter/le-grand-reportage-du-mardi-14-octobre-2025-4136495) (France Inter, 4 min)
- [Logiciel obsolète : l'État obligé de jeter des milliers d'ordinateurs ?](https://www.youtube.com/watch?v=76T8oubek-c) (France Info, 3 min)

### Le projet au lycée Carnot
- [Article du Café Pédagogique](https://www.cafepedagogique.net/2025/04/27/bruay-labuissiere-voyage-au-centre-du-libre-educatif/)
- [Linux, c'est facile !](https://tube-numerique-educatif.apps.education.fr/w/3LXem3XK4asbwZa5R1qGkW) (5 min)
- [Le projet NIRD présenté par les élèves](https://tube-numerique-educatif.apps.education.fr/w/pZCnzPKTYX2iF38Qh4ZGmq) (4 min)

## 📝 Licence

Ce projet est sous **licence libre** conformément aux exigences de la Nuit de l'Info 2025.

## 👥 Crédits

### Sujet porté par
- **Le collectif enseignant NIRD**
- **Le Bureau de la Nuit de l'Info 2025**

### Développement
- **MePrince47** - [@MePrince47](https://github.com/MePrince47)

### Remerciements
- Direction du numérique pour l'éducation
- Lycée Carnot de Bruay-la-Buissière
- Tous les acteurs de la communauté NIRD

---

🛡️ **Développé pour la Nuit de l'Info 2025** - Résistons ensemble à l'empire numérique !
