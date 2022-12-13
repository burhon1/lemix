from django.contrib import admin

from education.models import (
    Modules, Lessons, Contents, Resources, 
    Tests, Questions, Answers, FAQ
)

class QuestionInline(admin.TabularInline):
    model = Questions
    fields = ('question', 'ball',)
    extra = 0

class AnswerInline(admin.TabularInline):
    model = Answers
    fields = ('answer', 'is_right')
    extra = 0
@admin.register(Modules)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'order')
    list_display_links = ('id', 'title', 'author')
    list_filter = ('course', 'author')

    list_per_page: int = 50


@admin.register(Lessons)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'module', 'order', 'content_type')
    list_display_links = ('id', 'title', )
    list_filter = ('module', 'content_type', 'author')

    list_per_page: int = 50

@admin.register(Contents)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'lesson','author', 'order', 'content_type')
    list_display_links = ('id', 'title', )
    list_filter = ('lesson', 'content_type', 'author')

    list_per_page: int = 50

@admin.register(Resources)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'module', )
    list_display_links = ('id', 'lesson', )
    list_filter = ('lesson', 'module')

    list_per_page: int = 50

@admin.register(Tests)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'module', 'course')
    list_filter = ('lesson', 'module', 'course')

    list_per_page: int = 50

    inlines = [QuestionInline]

@admin.register(Questions)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'test', 'author')
    list_filter = ('test', 'author', 'ball')
    search_fields = ('question', )
    list_per_page: int = 50

    inlines = [AnswerInline]

@admin.register(Answers)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer')
    list_filter = ('question',)
    search_fields = ('question__question', 'answer')

    list_per_page: int = 50

admin.site.register(FAQ)