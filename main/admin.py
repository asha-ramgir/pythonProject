from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Topic)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['category','question', 'level']
admin.site.register(models.Questions, QuestionAdmin)

class UserSubmittedAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'user', 'submitted_answer']
admin.site.register(models.UserSubmittedAnswer, UserSubmittedAnswerAdmin)

class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'user']
admin.site.register(models.QuizAttempt, QuizAttemptAdmin)