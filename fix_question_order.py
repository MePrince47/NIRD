#!/usr/bin/env python
"""
Script pour corriger l'ordre des questions dans tous les quiz
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nird_Quiz.settings')
django.setup()

from NIRD.models import Quiz, Question

def fix_question_order():
    """Corrige l'ordre des questions pour tous les quiz"""
    
    print("🔧 Correction de l'ordre des questions...")
    print("─" * 60)
    
    quizzes = Quiz.objects.all()
    total_fixed = 0
    
    for quiz in quizzes:
        print(f"\n📝 Quiz: {quiz.title} (Niveau {quiz.level})")
        
        # Récupérer toutes les questions de ce quiz
        questions = list(quiz.questions.all())
        
        if not questions:
            print("   ⚠️  Aucune question trouvée")
            continue
        
        print(f"   Nombre de questions: {len(questions)}")
        
        # Vérifier si l'ordre est déjà correct
        orders = [q.order for q in questions]
        if orders == list(range(len(questions))):
            print("   ✅ Ordre déjà correct")
            continue
        
        # Corriger l'ordre
        print(f"   🔄 Correction de l'ordre...")
        for index, question in enumerate(questions):
            old_order = question.order
            question.order = index
            question.save()
            if old_order != index:
                print(f"      Question {index + 1}: order {old_order} → {index}")
                total_fixed += 1
        
        print(f"   ✅ Ordre corrigé: 0 à {len(questions) - 1}")
    
    print()
    print("=" * 60)
    print(f"✨ Correction terminée : {total_fixed} questions mises à jour")
    print("=" * 60)
    print()
    
    # Vérification finale
    print("🔍 Vérification finale:")
    for quiz in quizzes:
        questions = quiz.questions.all().order_by('order')
        if questions.exists():
            orders = list(questions.values_list('order', flat=True))
            expected = list(range(questions.count()))
            status = "✅" if orders == expected else "❌"
            print(f"   {status} {quiz.title}: {len(orders)} questions (ordre: {min(orders)}-{max(orders)})")
    print()

if __name__ == "__main__":
    fix_question_order()
