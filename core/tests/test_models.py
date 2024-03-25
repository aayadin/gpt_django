import pytest
from mixer.backend.django import mixer

from core.models import Question, QuestionTemplater, ResultTemplater, Vacancy


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
def test_vacancy_creation(vacancy):
    assert vacancy.name == 'Test vacancy name'
    assert vacancy.description == 'Test vacancy description'


@pytest.mark.django_db
def test_question_creation(question, vacancy):
    assert question.vacancy == vacancy
    assert question.text == 'Test question text'


@pytest.mark.django_db
def test_question_templater_prompt(question_templater, vacancy):
    expected_prompt = ('Vacancy name: Test vacancy name, '
                       'vacancy description: Test vacancy description')
    assert question_templater.prompt() == expected_prompt


@pytest.mark.django_db
def test_result_templater_prompt(result_templater, question):
    expected_prompt = ('Vacancy name: Test vacancy name, '
                       'vacancy description: Test vacancy description, '
                       'question text: Test question text, '
                       'answer text: None')
    assert result_templater.prompt() == expected_prompt


@pytest.mark.django_db
def test_result_templater_prompt_with_answer(result_templater, question):
    answer = 'Test answer'
    expected_prompt = ('Vacancy name: Test vacancy name, '
                       'vacancy description: Test vacancy description, '
                       'question text: Test question text, '
                       'answer text: Test answer')
    assert result_templater.prompt(answer) == expected_prompt
