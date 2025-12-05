# 🎯 Système de progression et déblocage automatique

## 📊 Comment fonctionne le système

### 1. Déblocage automatique des niveaux

**Règle de base :** Pour débloquer le niveau suivant, il faut **réussir** le niveau actuel avec au moins **60% de bonnes réponses**.

#### Exemple de progression
```
Utilisateur démarre au niveau 1
↓
Complète le quiz niveau 1 avec 70% → ✅ Réussi
↓
Niveau 2 débloqué automatiquement
↓
Complète le quiz niveau 2 avec 45% → ⚠️ Échec
↓
Niveau 2 reste accessible (peut refaire)
Niveau 3 reste verrouillé
↓
Refait le quiz niveau 2 avec 65% → ✅ Réussi
↓
Niveau 3 débloqué automatiquement
```

### 2. Calcul du niveau utilisateur

Le niveau de l'utilisateur est calculé automatiquement :

```python
niveau_utilisateur = max(niveaux_réussis) + 1
```

**Exemples :**
- Quiz 1 réussi (70%) → Niveau utilisateur = 2
- Quiz 1 et 2 réussis → Niveau utilisateur = 3
- Quiz 1, 2, 3 réussis → Niveau utilisateur = 4

### 3. Affichage de la progression

Pour chaque quiz, l'utilisateur voit :

#### ✅ Quiz réussi (≥ 60%)
```
✅ Réussi
85.0%
━━━━━━━━━━━━━━━━━━━━ (barre verte)
Meilleur score : 17/20 points
🔄 Refaire le niveau
```

#### ⚠️ Quiz tenté mais échoué (< 60%)
```
⚠️ À améliorer
45.0%
━━━━━━━━━━━━━━━━━━━━ (barre orange)
Meilleur score : 9/20 points
🔄 Refaire le niveau
```

#### 🔒 Quiz non tenté
```
Progression
0%
━━━━━━━━━━━━━━━━━━━━ (barre grise)
🚀 Commencer le niveau
```

#### 🔒 Quiz verrouillé
```
🔒 Niveau 3 requis
(bouton désactivé)
```

## 🔧 Modifications techniques

### Fichiers modifiés

#### 1. `NIRD/models.py` - UserProfile

**Nouvelle méthode `update_stats()`**
```python
def update_stats(self):
    # Calcule le niveau basé sur les quiz réussis (≥60%)
    # Niveau = max(quiz réussis) + 1
```

**Nouvelle méthode `get_quiz_progress(quiz)`**
```python
def get_quiz_progress(self, quiz):
    return {
        'completed': bool,      # Quiz déjà tenté ?
        'best_score': int,      # Meilleur score obtenu
        'max_score': int,       # Score maximum possible
        'percentage': float,    # Pourcentage (0-100)
        'passed': bool          # Réussi (≥60%) ?
    }
```

#### 2. `NIRD/views.py` - home()

Calcule la progression pour chaque quiz et la passe au template :

```python
quiz_progress = {}
for quiz in quizzes:
    quiz_progress[quiz.id] = user_profile.get_quiz_progress(quiz)
```

#### 3. `templates/NIRD/home.html`

Affiche dynamiquement :
- Pourcentage de réussite
- Barre de progression colorée (vert si réussi, orange si échoué)
- Meilleur score
- Statut (✅ Réussi, ⚠️ À améliorer, ou Progression)
- Bouton adapté (Commencer / Refaire / Verrouillé)

#### 4. `NIRD/templatetags/nird_filters.py` (nouveau)

Filtre personnalisé pour accéder aux dictionnaires dans les templates :

```python
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
```

## 🎮 Expérience utilisateur

### Scénario 1 : Nouvel utilisateur
1. Se connecte → Niveau 1
2. Voit uniquement le quiz niveau 1 débloqué
3. Tous les autres quiz sont verrouillés avec 🔒

### Scénario 2 : Progression normale
1. Complète le quiz niveau 1 avec 75%
2. Retourne à l'accueil
3. Voit :
   - Quiz 1 : ✅ Réussi - 75% - Meilleur score : 15/20
   - Quiz 2 : 🚀 Commencer le niveau (débloqué !)
   - Quiz 3+ : 🔒 Verrouillés

### Scénario 3 : Échec et réessai
1. Complète le quiz niveau 2 avec 40%
2. Retourne à l'accueil
3. Voit :
   - Quiz 2 : ⚠️ À améliorer - 40% - 🔄 Refaire
   - Quiz 3 : 🔒 Toujours verrouillé
4. Refait le quiz niveau 2 avec 70%
5. Quiz 3 se débloque automatiquement !

### Scénario 4 : Amélioration du score
1. Quiz déjà réussi avec 65%
2. Peut le refaire pour améliorer son score
3. Si nouveau score > ancien score → mise à jour
4. Le meilleur score est toujours affiché

## 📈 Avantages du système

### ✅ Pour l'utilisateur
- **Progression claire** : Sait exactement où il en est
- **Motivation** : Voit ses progrès visuellement
- **Récompense** : Déblocage automatique des niveaux
- **Amélioration** : Peut refaire pour améliorer son score
- **Feedback** : Sait s'il a réussi ou doit s'améliorer

### ✅ Pour la plateforme
- **Gamification** : Système de progression engageant
- **Pédagogie** : Force à maîtriser chaque niveau
- **Rétention** : Encourage à revenir pour s'améliorer
- **Équité** : Tout le monde suit le même parcours

## 🔍 Détails techniques

### Seuil de réussite : 60%

Pourquoi 60% ?
- **Pas trop facile** : Nécessite une vraie compréhension
- **Pas trop dur** : Reste accessible
- **Standard éducatif** : Correspond à une note de 12/20

### Calcul du pourcentage

```python
percentage = (score_obtenu / score_maximum) * 100
```

Exemple :
- 15 points obtenus sur 20 points max
- Pourcentage = (15 / 20) * 100 = 75%
- Résultat : ✅ Réussi

### Meilleur score

Le système garde toujours le **meilleur score** de toutes les tentatives :

```python
best_attempt = attempts.order_by('-score').first()
```

## 🧪 Tests recommandés

1. **Test de déblocage**
   - Créer un nouvel utilisateur
   - Vérifier qu'il est niveau 1
   - Compléter le quiz 1 avec 70%
   - Vérifier que le niveau passe à 2
   - Vérifier que le quiz 2 est débloqué

2. **Test d'échec**
   - Compléter un quiz avec 40%
   - Vérifier que le niveau suivant reste verrouillé
   - Vérifier l'affichage "⚠️ À améliorer"

3. **Test d'amélioration**
   - Compléter un quiz avec 65%
   - Le refaire avec 85%
   - Vérifier que le meilleur score est 85%

4. **Test de progression visuelle**
   - Vérifier les barres de progression
   - Vérifier les couleurs (vert/orange/gris)
   - Vérifier les pourcentages affichés

## 📝 Notes importantes

- **Mise à jour automatique** : Le profil se met à jour automatiquement après chaque quiz
- **Pas de régression** : Le niveau ne peut jamais baisser
- **Plusieurs tentatives** : Illimité, encouragé pour s'améliorer
- **Meilleur score conservé** : Seul le meilleur compte

## 🚀 Prochaines améliorations possibles

- 🏆 Badges pour 100% de réussite
- ⭐ Étoiles (1-3) selon le score
- 📊 Graphique de progression
- 🎖️ Classement par niveau
- 🔥 Streak de jours consécutifs
