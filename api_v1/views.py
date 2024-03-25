from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Answer, Question, QuestionTemplater, ResultTemplater
from core.queries import gpt_query
from core.validators import validate_result

from .validators import api_connection


@api_view(['POST'])
@api_connection
def generate_question(request):
    templater_id = request.GET.get('templater')
    templater = get_object_or_404(QuestionTemplater, id=templater_id)

    gpt_response = gpt_query(templater).choices[0].message.content

    if not gpt_response:
        return Response(
            {'error': 'Empty GPT response'},
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    question = Question(vacancy=templater.vacancy, text=gpt_response)
    question.save()

    return Response(gpt_response, status.HTTP_201_CREATED)


@api_view(['POST'])
@api_connection
def check_answer(request):
    question_id = request.GET.get('question')
    try:
        user_answer = request.data['user_answer']
    except KeyError:
        return Response(
            {'error': 'No user_answer found'},
            status.HTTP_400_BAD_REQUEST
        )
    templater = get_object_or_404(ResultTemplater, question=question_id)

    gpt_response = gpt_query(
        templater,
        answer=user_answer
    ).choices[0].message.content

    if not gpt_response:
        return Response(
            {'error': 'Empty GPT response'},
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    validate_result(gpt_response)
    answer = Answer(
        question_id=question_id,
        text=user_answer,
        result=gpt_response
    )
    answer.save()

    return Response(gpt_response, status.HTTP_201_CREATED)
