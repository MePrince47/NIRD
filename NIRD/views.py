from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import Quiz, Question, UserQuizAttempt, UserAnswer


# Page d'accueil avec tous les quiz
def home(request):
    quizzes = Quiz.objects.all().order_by('level')
    return render(request, "NIRD/home.html", {"quizzes": quizzes})


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


# Démarrer un quiz
@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt, _ = UserQuizAttempt.objects.get_or_create(user=request.user, quiz=quiz)
    first_question = quiz.questions.order_by('order').first()
    if first_question:
        return redirect('question', attempt_id=attempt.id, question_id=first_question.id)
    return redirect('home')


# Afficher une question et gérer la réponse
@login_required
def question_view(request, attempt_id, question_id):
    attempt = get_object_or_404(UserQuizAttempt, id=attempt_id, user=request.user)
    question = get_object_or_404(Question, id=question_id, quiz=attempt.quiz)

    if request.method == "POST":
        selected_index = int(request.POST.get("answer", -1))
        correct = question.is_correct(selected_index)

        UserAnswer.objects.update_or_create(
            attempt=attempt,
            question=question,
            defaults={"selected_index": selected_index, "correct": correct}
        )

        if correct:
            attempt.score += question.points
            attempt.save()

        # Passer à la question suivante
        next_question = attempt.quiz.questions.filter(order__gt=question.order).order_by('order').first()
        if next_question:
            return redirect('question', attempt_id=attempt.id, question_id=next_question.id)
        else:
            attempt.completed = True
            attempt.save()
            return redirect('quiz_result', attempt_id=attempt.id)

    return render(request, "NIRD/question.html", {"question": question, "time_limit": question.time_limit})


# Page résultat
@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(UserQuizAttempt, id=attempt_id, user=request.user)
    return render(request, "NIRD/result.html", {"attempt": attempt})
