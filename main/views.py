from django.shortcuts import render
from django.http import HttpResponse
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from random import shuffle
import ast
from datetime import datetime


# Create your views here.
def home(request):
    return render(request, 'home.html')


def register(request):
    msg = None
    form = forms.RegisterUser
    if request.method == 'POST':
        form = forms.RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            msg = 'Data has been added'
    return render(request, 'registration/register.html', {'form': form, 'msg': msg})


def hello(request):
    return render(request, 'home.html')


def all_topics(request):
    topicData = models.Topic.objects.all()
    return render(request, 'all_topics.html', {'data': topicData})


@login_required()
def topic_questions(request, topic_id):
    topic = models.Topic.objects.get(id=topic_id)
    questions = models.Questions.objects.filter(category=topic)
    question_ids = list(questions.values_list('id', flat=True))
    shuffle(question_ids)
    possible_ids = question_ids[:5]
    random_questions = questions.filter(pk__in=possible_ids)
    first_question = random_questions.first()
    quiz_attempt_id = models.QuizAttempt.objects.create(user=request.user, category=topic, score=0, status='incomplete',
                                                        attempt_date=datetime.now()).id
    return render(request, 'topic_questions.html', {'question': first_question, 'category': topic,
                                                    'random_question_ids': possible_ids,
                                                    'quiz_attempt_id': quiz_attempt_id})


@login_required()
def submit_answer(request, quiz_attempt_id, topic_id, quest_id, random_question_ids):
    if request.method == 'POST':
        random_question_ids = ast.literal_eval(random_question_ids)
        random_question_ids.remove(quest_id)
        topic = models.Topic.objects.get(id=topic_id)
        quiz_attempt = models.QuizAttempt.objects.get(id=quiz_attempt_id)
        question = models.Questions.objects.filter(category=topic, id__in=random_question_ids).first()
        if 'skip' in request.POST:
            quest = models.Questions.objects.get(id=quest_id)
            user = request.user
            answer = 'Not submitted'
            models.UserSubmittedAnswer.objects.create(user=user, question=quest, submitted_answer=answer,
                                                      quiz_attempt=quiz_attempt)
            if question:
                return render(request, 'topic_questions.html', {'question': question, 'category': topic,
                                                                'random_question_ids': random_question_ids,
                                                                'quiz_attempt_id': quiz_attempt_id})
        else:
            quest = models.Questions.objects.get(id=quest_id)
            user = request.user
            answer = request.POST['answer']
            models.UserSubmittedAnswer.objects.create(user=user, question=quest, submitted_answer=answer,
                                                      quiz_attempt=quiz_attempt)
        if question:
            return render(request, 'topic_questions.html', {'question': question, 'category': topic,
                                                            'random_question_ids': random_question_ids,
                                                            'quiz_attempt_id': quiz_attempt_id})
        else:
            result = models.UserSubmittedAnswer.objects.filter(user=request.user, quiz_attempt=quiz_attempt_id)

            correct_answers = 0
            for row in result:
                if row.question.right_option == row.submitted_answer:
                    correct_answers += 1
            percentage = round((correct_answers * 100) / result.count(), 2)
            if correct_answers == 5:
                display_text = 'You are genius!'
            elif correct_answers == 4:
                display_text = 'Excellent work!'
            elif correct_answers == 3:
                display_text = 'Good job!'
            else:
                display_text = 'Please try again!'
            quiz_attempt.status = 'complete'
            quiz_attempt.score = correct_answers
            quiz_attempt.save()
        return render(request, 'result.html', {'result': result,
                                               'correct_answers': correct_answers,
                                               'percentage': percentage, 'display_text': display_text,
                                               'topic_id': topic_id})
    else:
        return HttpResponse('Method not allowed')


def scores(request):
    result = models.QuizAttempt.objects.filter(user=request.user, status='complete')
    highest_score = average_score = lowest_score = 0
    if result:
        highest_score = 0
        lowest_score = 5
        sum = 0
        for row in result:
            sum += row.score
            if row.score > highest_score:
                highest_score = row.score
            if row.score < lowest_score:
                lowest_score = row.score
        average_score = sum / result.count()
    return render(request, 'scores.html', {'result': result, 'average_score': average_score,
                                           'highest_score': highest_score, 'lowest_score': lowest_score})
