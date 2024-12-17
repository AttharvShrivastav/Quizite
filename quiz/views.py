from django.shortcuts import render, redirect
from .models import Question, Option, Leaderboard
import random

def landing_page(request):
    return render(request, 'quiz/landing.html')

def start_quiz(request):
    # Clear previous session data
    request.session['score'] = 0
    request.session['answered_questions'] = []
    request.session['wrong_answers'] = []
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

        # Retrieve the current question and selected option
        question = Question.objects.get(id=question_id)
        selected_option = Option.objects.get(id=selected_option_id)

        # Track answered questions and wrong answers
        answered_questions = request.session.get('answered_questions', [])
        wrong_answers = request.session.get('wrong_answers', [])

        # Check if the selected answer is correct
        if not selected_option.is_correct:
            wrong_answers.append({
                'question': question.text,
                'selected_option': selected_option.text,
                'correct_option': question.options.get(is_correct=True).text
            })

        # Append the question to the answered list
        answered_questions.append(question_id)
        request.session['answered_questions'] = answered_questions
        request.session['wrong_answers'] = wrong_answers

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

def quiz_summary(request):
    score = len(request.session.get('answered_questions', [])) - len(request.session.get('wrong_answers', []))
    total_questions = len(request.session.get('answered_questions', []))
    wrong_answers = request.session.get('wrong_answers', [])

    return render(request, 'quiz/summary.html', {
        'score': score,
        'total_questions': total_questions,
        'wrong_answers': wrong_answers,
    })

