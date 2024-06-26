# Generated by Django 5.0.3 on 2024-03-23 15:05

import django.db.models.deletion
from django.db import migrations, models

import core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=5000, verbose_name='Текст вопроса')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название вакансии')),
                ('description', models.TextField(max_length=5000, verbose_name='Описание вакансии')),
            ],
            options={
                'verbose_name': 'Вакансия',
                'verbose_name_plural': 'Вакансии',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=5000, verbose_name='Ответ на вопрос')),
                ('result', models.IntegerField(validators=[core.validators.validate_result], verbose_name='Результат')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.question')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ResultTemplater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system', models.TextField(max_length=5000)),
                ('prompt_text', models.TextField(max_length=5000)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.question')),
            ],
            options={
                'verbose_name': 'Шаблон для получения результата',
                'verbose_name_plural': 'Шаблоны для получения результатов',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='QuestionTemplater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system', models.TextField(max_length=5000)),
                ('prompt_text', models.TextField(max_length=5000)),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.vacancy')),
            ],
            options={
                'verbose_name': 'Шаблон для получения вопроса',
                'verbose_name_plural': 'Шаблоны для получения вопросов',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='question',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.vacancy'),
        ),
    ]
