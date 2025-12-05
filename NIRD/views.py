from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    Quiz, Question, UserQuizAttempt, UserAnswer,
    QuizTip, UserProfile, Post, Comment, Like
)


# Page d'accueil avec tous les quiz
def home(request):
    quizzes = Quiz.objects.all().order_by('level')
    
    # Si l'utilisateur est connecté, récupérer son profil
    user_profile = None
    if request.user.is_authenticated:
        user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    return render(request, "NIRD/home.html", {
        "quizzes": quizzes,
        "user_profile": user_profile
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


# Démarrer un quiz
@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    # Vérifier si l'utilisateur a le niveau requis
    # Le niveau du quiz doit être <= au niveau de l'utilisateur
    if quiz.level > user_profile.level:
        # Rediriger vers l'accueil avec un message (on pourrait ajouter un message Django)
        from django.contrib import messages
        messages.warning(request, f"🔒 Tu dois atteindre le niveau {quiz.level} pour débloquer ce quiz ! Continue à jouer pour progresser.")
        return redirect('home')
    
    # Supprimer les tentatives non complétées pour ce quiz
    UserQuizAttempt.objects.filter(user=request.user, quiz=quiz, completed=False).delete()
    
    # Créer une nouvelle tentative
    attempt = UserQuizAttempt.objects.create(user=request.user, quiz=quiz)
    first_question = quiz.questions.order_by('order').first()
    if first_question:
        return redirect('question', attempt_id=attempt.id, question_id=first_question.id)
    return redirect('home')


# Afficher une question et gérer la réponse
@login_required
def question_view(request, attempt_id, question_id):
    attempt = get_object_or_404(UserQuizAttempt, id=attempt_id, user=request.user)
    question = get_object_or_404(Question, id=question_id, quiz=attempt.quiz)
    
    # Récupérer le tip pour cette question
    answered_count = attempt.answers.count()
    quiz_tip = attempt.quiz.tips.filter(trigger_question_number=answered_count).first()

    if request.method == "POST":
        selected_index = int(request.POST.get("answer", -1))
        correct = question.is_correct(selected_index)

        # Vérifier si cette question a déjà été répondue
        existing_answer = UserAnswer.objects.filter(attempt=attempt, question=question).first()
        
        if existing_answer:
            # Si la réponse existe déjà, on la met à jour sans modifier le score
            existing_answer.selected_index = selected_index
            existing_answer.correct = correct
            existing_answer.save()
        else:
            # Créer une nouvelle réponse et ajouter les points si correct
            UserAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_index=selected_index,
                correct=correct
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
            
            # Mettre à jour les stats du profil utilisateur
            request.user.profile.update_stats()
            
            return redirect('quiz_result', attempt_id=attempt.id)

    return render(request, "NIRD/question.html", {
        "question": question,
        "time_limit": question.time_limit,
        "quiz_tip": quiz_tip,
        "answered_count": answered_count
    })


# Page résultat
@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(UserQuizAttempt, id=attempt_id, user=request.user)
    total_questions = attempt.quiz.questions.count()
    correct_answers = attempt.answers.filter(correct=True).count()
    percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    return render(request, "NIRD/result.html", {
        "attempt": attempt,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "percentage": percentage
    })


# ========== RÉSEAU SOCIAL ==========

# Feed du réseau social
@login_required
def social_feed(request):
    posts = Post.objects.all().select_related('author', 'author__profile').prefetch_related('likes', 'comments')
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    return render(request, "NIRD/social_feed.html", {
        "posts": posts,
        "user_profile": user_profile
    })


# Créer un post
@login_required
@require_POST
def create_post(request):
    content = request.POST.get('content', '').strip()
    related_quiz_id = request.POST.get('related_quiz')
    
    if content:
        post = Post.objects.create(
            author=request.user,
            content=content,
            related_quiz_id=related_quiz_id if related_quiz_id else None
        )
        return redirect('social_feed')
    
    return redirect('social_feed')


# Liker un post
@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        # Si le like existe déjà, on le supprime (unlike)
        like.delete()
        liked = False
    else:
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'like_count': post.like_count()
        })
    
    return redirect('social_feed')


# Commenter un post
@login_required
@require_POST
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content', '').strip()
    parent_id = request.POST.get('parent_comment')
    
    if content:
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
            parent_comment_id=parent_id if parent_id else None
        )
    
    return redirect('social_feed')


# Supprimer un post
@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return redirect('social_feed')


# ========== CLASSEMENT / LEADERBOARD ==========

@login_required
def leaderboard(request):
    # Filtres
    period = request.GET.get('period', 'all')  # all, today, week, month
    
    # Base queryset
    profiles = UserProfile.objects.select_related('user').annotate(
        quiz_count=Count('user__userquizattempt', filter=Q(user__userquizattempt__completed=True))
    )
    
    # Filtre par période
    if period == 'today':
        today = timezone.now().date()
        profiles = profiles.filter(
            user__userquizattempt__answers__created_at__date=today
        ).distinct()
    elif period == 'week':
        week_ago = timezone.now() - timedelta(days=7)
        profiles = profiles.filter(
            user__userquizattempt__answers__created_at__gte=week_ago
        ).distinct()
    elif period == 'month':
        month_ago = timezone.now() - timedelta(days=30)
        profiles = profiles.filter(
            user__userquizattempt__answers__created_at__gte=month_ago
        ).distinct()
    
    # Trier par points
    profiles = profiles.order_by('-total_points', '-level')
    
    # Position de l'utilisateur actuel
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user_rank = list(profiles.values_list('id', flat=True)).index(user_profile.id) + 1 if user_profile.id in profiles.values_list('id', flat=True) else None
    
    return render(request, "NIRD/leaderboard.html", {
        "profiles": profiles[:50],  # Top 50
        "user_profile": user_profile,
        "user_rank": user_rank,
        "period": period
    })


# Profil utilisateur
@login_required
def user_profile(request, username):
    from django.contrib.auth.models import User
    user = get_object_or_404(User, username=username)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    
    # Statistiques
    attempts = UserQuizAttempt.objects.filter(user=user, completed=True)
    posts = Post.objects.filter(author=user)
    
    return render(request, "NIRD/user_profile.html", {
        "profile_user": user,
        "profile": profile,
        "attempts": attempts,
        "posts": posts
    })
