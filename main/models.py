from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=100)
    detail = models.TextField()

    # image = models.ImageField(upload_to='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Topic'

        def __str__(self):
            return self.title


class Questions(models.Model):
    category = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question = models.TextField()
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)
    level = models.CharField(max_length=100)
    time_limit = models.IntegerField()
    right_option = models.CharField(max_length=200)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = 'Question'

        def __str__(self):
            return self.question


class QuizAttempt(models.Model):
    attempt_date = models.DateTimeField()
    category = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    status = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Quiz Attempt'


class UserSubmittedAnswer(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_answer = models.CharField(max_length=200)
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'User Submitted Answers'
