from django.urls import path

from .views import check_answer, generate_question

app_name = 'api_v1'

urlpatterns = [
    path('check_answer', check_answer, name='check_answer'),
    path('generate_question', generate_question, name='generate_question'),
]
