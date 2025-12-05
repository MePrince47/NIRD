from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import Quiz, Question, UserQuizAttempt, UserAnswer
import random
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from django.db.models import Max

def viewsroad(request):
    return render(request, "NIRD/road.html")    

# Page d'accueil avec tous les quiz
def home(request):
    quizzes = Quiz.objects.all().order_by('level')

    # Top 5 scores utilisateurs
    top_scores = (
        UserQuizAttempt.objects
        .filter(user__isnull=False)  # ignorer anonymes
        .values('user')  
        .annotate(best_score=Max('score'))  
        .order_by('-best_score')[:5]  # top 5
    )

    # Ajouter le nom d'utilisateur pour affichage
    results = []
    for entry in top_scores:
        user_id = entry['user']
        score = entry['best_score']
        try:
            user = User.objects.get(id=user_id)
            username = user.username
        except User.DoesNotExist:
            username = "Unknown"
        results.append({"username": username, "score": score})

    return render(request, "NIRD/home.html", {
        "quizzes": quizzes,
        "top_scores": results
    })
# Login utilisateur si pas encore connecté
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, "NIRD/login.html", {"form": form})
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, "NIRD/signup.html", {"form": form})

# Démarrer un quiz

def start_quiz(request, level):
    quizzes = Quiz.objects.filter(level=level)
    if not quizzes.exists():
        return redirect('home')

    quiz = random.choice(list(quizzes))

    # Gestion tentative anonyme ou connectée
    if request.user.is_authenticated:
        attempt, created = UserQuizAttempt.objects.get_or_create(user=request.user, quiz=quiz)
    else:
        # utilisateur anonyme → on utilise id fictif 50
        attempt_id = request.session.get('attempt_id')
        if attempt_id:
            attempt = get_object_or_404(UserQuizAttempt, id=attempt_id)
        else:
            attempt = UserQuizAttempt.objects.create(
                quiz=quiz,
                user_id=50  # ID fictif pour anonyme
            )
            request.session['attempt_id'] = attempt.id

    # Sélection aléatoire de 5 questions
    questions = list(quiz.questions.all())
    if not questions:
        return redirect('home')

    if not attempt.selected_questions:
        random.shuffle(questions)
        attempt.selected_questions = [q.id for q in questions[:5]]
        attempt.save()

    first_question_id = attempt.selected_questions[0]
    return redirect('question', attempt_id=attempt.id, question_id=first_question_id)

def question_view(request, attempt_id, question_id):
    attempt = get_object_or_404(UserQuizAttempt, id=attempt_id)
    question = get_object_or_404(Question, id=question_id)

    # Si l'utilisateur se connecte après avoir commencé le quiz
    if request.user.is_authenticated and (attempt.user is None or attempt.user.id == 50):
        # On transfère la tentative à l'utilisateur connecté
        attempt.user = request.user
        # Si score temporaire existait, l'ajouter au vrai score
        if hasattr(attempt, 'score_temp'):
            attempt.score += attempt.score_temp
            delattr(attempt, 'score_temp')  # on supprime la variable temporaire
        attempt.save()

    error = None
    if request.method == "POST":
        selected_answer = request.POST.get("answer")
        if selected_answer is None:
            error = "Veuillez sélectionner une réponse avant de continuer."
        else:
            selected_index = int(selected_answer)
            correct = question.is_correct(selected_index)

            UserAnswer.objects.update_or_create(
                attempt=attempt,
                question=question,
                defaults={"selected_index": selected_index, "correct": correct}
            )

            # Gestion du score temporaire pour utilisateurs anonymes
            if attempt.user is None or attempt.user.id == 50:
                if not hasattr(attempt, 'score_temp'):
                    attempt.score_temp = 0
                if correct:
                    attempt.score_temp += question.points
            else:
                if correct:
                    attempt.score += question.points
                    attempt.save()

            # Question suivante
            ids = attempt.selected_questions
            try:
                next_index = ids.index(question.id) + 1
                next_question_id = ids[next_index]
                return redirect('question', attempt_id=attempt.id, question_id=next_question_id)
            except (ValueError, IndexError):
                attempt.completed = True
                # Si score temporaire existait pour utilisateur anonyme, on l'affiche à la fin
                if hasattr(attempt, 'score_temp'):
                    attempt.final_score = attempt.score_temp
                else:
                    attempt.final_score = attempt.score
                attempt.save()
                return redirect('quiz_result', attempt_id=attempt.id)

    return render(request, "NIRD/question.html", {
        "question": question,
        "time_limit": question.time_limit,
        "error": error
    })

def quiz_result(request, attempt_id):
    attempt = get_object_or_404(UserQuizAttempt, id=attempt_id)

    next_level = attempt.quiz.level + 1
    next_quizzes = Quiz.objects.filter(level=next_level)

    return render(request, "NIRD/result.html", {
        "attempt": attempt,
        "next_quizzes_exist": next_quizzes.exists(),
        "next_level": next_level,
        "is_anonymous": attempt.user is None or attempt.user.id == 50
    })

# Afficher une question et gérer la réponse

def question_view(request, attempt_id, question_id):
    # Ne pas filtrer sur user si l'utilisateur n'est pas connecté
    attempt = get_object_or_404(UserQuizAttempt, id=attempt_id)
    question = get_object_or_404(Question, id=question_id)

    # Si l'utilisateur se connecte après avoir commencé le quiz
    if request.user.is_authenticated and (attempt.user is None or attempt.user.id == 50):
        attempt.user = request.user
        attempt.save()

    error = None
    if request.method == "POST":
        selected_answer = request.POST.get("answer")
        if selected_answer is None:
            error = "Veuillez sélectionner une réponse avant de continuer."
        else:
            selected_index = int(selected_answer)
            correct = question.is_correct(selected_index)

            UserAnswer.objects.update_or_create(
                attempt=attempt,
                question=question,
                defaults={"selected_index": selected_index, "correct": correct}
            )

            if correct:
                attempt.score += question.points
                attempt.save()

            # Question suivante
            ids = attempt.selected_questions
            try:
                next_index = ids.index(question.id) + 1
                next_question_id = ids[next_index]
                return redirect('question', attempt_id=attempt.id, question_id=next_question_id)
            except (ValueError, IndexError):
                attempt.completed = True
                attempt.save()
                return redirect('quiz_result', attempt_id=attempt.id)

    return render(request, "NIRD/question.html", {
        "question": question,
        "time_limit": question.time_limit,
        "error": error
    })

def signup(request):
    attempt_id = request.GET.get('attempt_id')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # transférer le score temporaire
            if attempt_id:
                from .models import UserQuizAttempt
                attempt = UserQuizAttempt.objects.get(id=attempt_id)
                if attempt.user is None or attempt.user.id == 50:
                    attempt.user = user
                    if hasattr(attempt, 'score_temp'):
                        attempt.score += attempt.score_temp
                        delattr(attempt, 'score_temp')
                    attempt.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, "NIRD/signup.html", {"form": form})

from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import UserQuizAttempt

def leaderboard(request):
    # Récupérer la somme des scores pour chaque utilisateur
    top_scores = (
        UserQuizAttempt.objects
        .values('user')  # grouper par utilisateur (None pour anonymes)
        .annotate(total_score=Sum('score'))  # somme des scores par utilisateur
        .order_by('-total_score')  # tri décroissant
    )

    # Ajouter le nom d'utilisateur pour affichage
    results = []
    for entry in top_scores:
        user_id = entry['user']
        score = entry['total_score']

        if user_id is None:
            username = "Anonymous"
        else:
            try:
                user = User.objects.get(id=user_id)
                username = user.username
            except User.DoesNotExist:
                username = "Unknown"

        results.append({
            "username": username,
            "score": score
        })

    return render(request, "NIRD/leaderboard.html", {"top_scores": results})
