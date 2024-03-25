from django.contrib import admin

from .models import (Answer, Question, QuestionTemplater, ResultTemplater,
                     Vacancy)


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'vacancy', 'text')
    search_fields = ('vacancy',)


class QuestionTemplaterAdmin(admin.ModelAdmin):
    list_display = ('id', 'vacancy', 'system', 'prompt_text')
    search_fields = ('id', 'vacancy')


class ResultTemplaterAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'system', 'prompt_text')
    search_fields = ('id', 'question')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'result')
    search_fields = ('question',)


admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionTemplater, QuestionTemplaterAdmin)
admin.site.register(ResultTemplater, ResultTemplaterAdmin)
admin.site.register(Answer, AnswerAdmin)
