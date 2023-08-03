from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Question, Answer, Comment, Category


class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 1


class QuestionAdmin(admin.ModelAdmin):  # 검색 추가
    search_fields = ['subject']
    empty_value_display = '-empty-'
    list_display = ['subject', 'author', 'create_date', 'modify_date']


class AnswerAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['content', 'author', 'create_date', 'modify_date']


class CommentAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['content', 'author', 'create_date']


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['subject']
    empty_value_display = '-empty-'
    list_display = ['subject']
    inlines = [
        QuestionInLine,
    ]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)

