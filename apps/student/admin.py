from django.contrib import admin

from .models import Homeworks, TestResults, StudentAnswers


@admin.register(Homeworks)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'student', 'ball')


@admin.register(TestResults)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'student', 'ball')


@admin.register(StudentAnswers)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'student',)
