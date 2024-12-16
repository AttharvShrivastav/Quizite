from django.shortcuts import render, redirect
from .models import Question, Option, Leaderboard
import random

def start_quiz(request):
    # Initialize session data
    request.session['score'] = 0
    request.session['answered_questions'] = []
    return redirect('quiz:fetch_question')

def fetch_question(request):
    answered_questions = request.session.get('answered_questions', [])
    question = Question.objects.exclude(id__in=answered_questions).order_by('?').first()

    if question:
        request.session['current_question'] = question.id
        options = question.options.all()
        return render(request, 'quiz/question.html', {'question': question, 'options': options})
    else:
        return redirect('quiz:summary')

def submit_answer(request):
    if request.method == 'POST':
        question_id = request.session.get('current_question')
        selected_option_id = request.POST.get('option')
        selected_option = Option.objects.get(id=selected_option_id)

        if selected_option.is_correct:
            request.session['score'] += 1

        answered_questions = request.session.get('answered_questions', [])
        answered_questions.append(question_id)
        request.session['answered_questions'] = answered_questions

        return redirect('quiz:fetch_question')

def quiz_summary(request):
    score = request.session.get('score', 0)
    total_questions = len(request.session.get('answered_questions', []))
    user = request.session.get('username', 'Anonymous')
    Leaderboard.objects.create(user=user, score=score)

    return render(request, 'quiz/summary.html', {
        'score': score,
        'total_questions': total_questions
    })

def leaderboard(request):
    top_scores = Leaderboard.objects.order_by('-score')[:10]
    return render(request, 'quiz/leaderboard.html', {'top_scores': top_scores})
