from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST

from questioning.qa.models import Question, Answer
from questioning.utils.helpers import ajax_required, AuthorRequiredMixin
from questioning.qa.forms import QuestionForm


class QuestionListView(LoginRequiredMixin, ListView):
    '''所有问题的页面'''
    queryset = Question.objects.all()
    paginate_by = 10
    context_object_name = 'questions'
    template_name = 'qa/question_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionListView, self).get_context_data(
            object_list=None, **kwargs)
        context['popular_tags'] = Question.objects.get_counted_tags()
        context['active'] = 'all'
        return context


class AnsweredQuestionListView(QuestionListView):
    '''已经有答案的问题'''

    def get_queryset(self):
        return Question.objects.get_answered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AnsweredQuestionListView, self).get_context_data(
            object_list=None, **kwargs)
        context['active'] = 'answered'
        return context


class UnAnsweredQuestionListView(QuestionListView):
    '''没有答案的问题'''

    def get_queryset(self):
        return Question.objects.get_unanswered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UnAnsweredQuestionListView, self).get_context_data(
            object_list=None, **kwargs)
        context['active'] = 'unanswered'
        return context
