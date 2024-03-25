from django.db import models

import core.constants as c
from core.validators import validate_result


class Vacancy(models.Model):
    """
    Модель для создания вакансии. Создать можно через админку.
    Вакансия используется в QuestionTemplater.
    """
    name = models.CharField('Название вакансии', max_length=c.MAX_CHARFIELD)
    description = models.TextField('Описание вакансии', max_length=c.MAX_TEXTFIELD)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Question(models.Model):
    """
    Модель вопроса. Вопрос создается при успещном запросе к ChatGPT с
    использованием QuestionTemplater.
    """
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    text = models.TextField('Текст вопроса', max_length=c.MAX_TEXTFIELD)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-id']

    def __str__(self):
        return self.text[:c.MAX_STR]


class Templater(models.Model):
    """
    Абстрактная модель для создания QuestionTemplater и ResultTemplater.
    Для передачи в ChatGPT системной информации используется system,
    для передачи user-информации исрользуется prompt.
    В дочерних классах метод prompt переопределен.
    """
    system = models.TextField(max_length=c.MAX_TEXTFIELD)
    prompt_text = models.TextField(max_length=c.MAX_TEXTFIELD)

    def prompt(self, *args):
        return self.prompt_text

    class Meta:
        abstract = True

    def __str__(self):
        return self.prompt()[:c.MAX_STR] + '...'


class QuestionTemplater(Templater):
    """
    Шаблонизатор запроса для получения из ChatGPT сгенерированного вопроса
    для вакансии. Шаблон создается через админку. При создании в тексте
    prompt_text нужно вставить два раза '{}'. Метод prompt подставляет вместо
    '{}' название вакансии и ее описание. Важно в тексте запроса
    сохранять порядок аргументов.
    """
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)

    def prompt(self, *args) -> str:
        return self.prompt_text.format(
            self.vacancy.name,
            self.vacancy.description
        )

    class Meta:
        verbose_name = 'Шаблон для получения вопроса'
        verbose_name_plural = 'Шаблоны для получения вопросов'
        ordering = ['-id']


class ResultTemplater(Templater):
    """
    Шаблонизатор запроса для получения из ChatGPT оценки ответа.
    Шаблон создается через админку. При создании в тексте
    prompt_text нужно вставить три раза '{}'. Метод prompt подставляет вместо
    '{}' название вакансии, ее описание и вопрос. Четвертый аргумент (ответ,
    который нужно оценить), подставляется из тела запроса пользователя.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def prompt(self, answer_text=None) -> str:
        return self.prompt_text.format(
            self.question.vacancy.name,
            self.question.vacancy.description,
            self.question.text,
            answer_text
        )

    class Meta:
        verbose_name = 'Шаблон для получения результата'
        verbose_name_plural = 'Шаблоны для получения результатов'
        ordering = ['-id']


class Answer(models.Model):
    """
    Модель ответа, содержащая оценку (результат) от 1 до 10.
    Создается при успешном запросе с использованием ResultTemplater.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField('Ответ на вопрос', max_length=5000)
    result = models.IntegerField('Результат', validators=[validate_result])

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['-id']

    def __str__(self):
        return self.text[:c.MAX_STR]
