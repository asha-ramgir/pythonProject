from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/register/', views.register, name='register'),
    path('all-topics', views.all_topics, name='all_topics'),
    path('topic-questions/<int:topic_id>', views.topic_questions, name='topic_questions'),
    path('submit-answer/<int:quiz_attempt_id>/<int:topic_id>/<int:quest_id>/<str:random_question_ids>', views.submit_answer, name='submit_answer'),
    path('scores', views.scores, name='scores'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
