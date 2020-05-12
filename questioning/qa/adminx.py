from questioning.qa.models import Question, Answer

import xadmin


class QuestionAdmin:
    list_display = ['title', 'user','status', 'has_answer']
    list_filter = ['title', 'tags', 'created_at']
    search_fields = ['title', 'content']
    ordering = ['-created_at']
    readonly_fields = ['status', 'user', 'has_answer']


class AnswerAdmin:
    list_display = ['content', 'question','is_answer', 'user']
    list_filter = ['content', 'is_answer', 'question']
    search_fields = ['content']
    ordering = ['-created_at']
    readonly_fields = ['is_answer', 'user', 'question']

xadmin.site.register(Question, QuestionAdmin)
xadmin.site.register(Answer, AnswerAdmin)
