from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

import pytest
from mixer.backend.django import mixer
from openai.types.chat.chat_completion import ChatCompletion, Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from core.models import Question, QuestionTemplater, ResultTemplater, Vacancy


def mock_gpt_response(message: str) -> ChatCompletion:
    """
    Создание мокового объекта класса ChatCompletion (ответ от ChatGPT)
    """
    message = ChatCompletionMessage(role='assistant', content=message)
    choice = Choice(index=1, message=message, finish_reason='stop')
    completion = ChatCompletion(id='id', choices=[choice,], created=1, model='model', object="chat.completion")
    return completion


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def vacancy():
    return mixer.blend(
        Vacancy,
        name='Test vacancy name',
        description='Test vacancy description'
    )


@pytest.fixture
def question(vacancy):
    return mixer.blend(
        Question,
        vacancy=vacancy,
        text='Test question text'
    )


@pytest.fixture
def question_templater(vacancy):
    return mixer.blend(
        QuestionTemplater,
        vacancy=vacancy,
        system='Question templater test system',
        prompt_text='Vacancy name: {}, vacancy description: {}'
    )


@pytest.fixture
def result_templater(question):
    return mixer.blend(
        ResultTemplater,
        question=question,
        system='Result templater test system',
        prompt_text=('Vacancy name: {}, vacancy description: {}, '
                     'question text: {}, answer text: {}')
    )


@pytest.mark.django_db
def test_check_answer_success(mocker, api_client, question, result_templater):
    mocked_value = mock_gpt_response('10')
    mocker.patch('core.queries.gpt_query', return_value=mocked_value)

    url = reverse('api_v1:check_answer') + f'?question={question.id}'
    data = {'user_answer': 'Test answer'}
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED or status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_check_answer_missing_question_id(api_client, question):
    url = reverse('api_v1:check_answer') + f'?question={question.id + 1}'
    data = {'user_answer': 'Test answer'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND or status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_generate_question_success(mocker, api_client, question_templater):
    mocked_value = mock_gpt_response('Test question')
    mocker.patch('core.queries.gpt_query', return_value=mocked_value)

    url = reverse('api_v1:generate_question') + f'?templater={question_templater.id}'
    response = api_client.post(url)

    assert response.status_code == status.HTTP_201_CREATED or status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_generate_question_missing_templater_id(api_client, question_templater):
    url = reverse('api_v1:generate_question') + f'?templater={question_templater.id + 1}'
    response = api_client.post(url, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND or status.HTTP_403_FORBIDDEN
