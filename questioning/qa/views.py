from decimal import Decimal

import markdown
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST

from questioning.notifications.views import push_notification
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


class CreateQuestionView(LoginRequiredMixin, CreateView):
    '''新增问题'''
    model = Question
    form_class = QuestionForm
    template_name = 'qa/question_form.html'
    message = '问题已经发布'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateQuestionView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy('qa:unanswered_q')


class QuestionDetailView(LoginRequiredMixin, DetailView):
    '''问题详情内容'''
    model = Question
    template_name = 'qa/question_detail.html'
    context_object_name = 'question'

    def get_queryset(self):
        return Question.objects.filter(pk=self.kwargs['pk'])


class QuestionDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    '''问题删除'''
    model = Question
    context_object_name = 'question'
    template_name = 'qa/question_confirm_delete.html'
    success_url = reverse_lazy('qa:unanswered_q')


class QuestionUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    '''问题编辑'''
    model = Question
    context_object_name = 'question'
    template_name = 'qa/question_update.html'
    form_class = QuestionForm
    message = '编辑成功'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(QuestionUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy('qa:question_detail', kwargs={
            'pk': self.kwargs['pk']
        })


class CreateAnswerView(LoginRequiredMixin, CreateView):
    '''回答问题'''
    model = Answer
    fields = ['content']
    message = '回答已提交'
    template_name = 'qa/answer_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(CreateAnswerView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy('qa:question_detail', kwargs={
            'pk': self.kwargs['question_id']
        })


@login_required
@ajax_required
@require_POST
def question_vote(request):
    '''给问题投票'''
    question_id = request.POST['question']
    value = True if request.POST['value'] == 'U' else False
    question = Question.objects.get(pk=question_id)
    users = question.votes.values_list('user', flat=True)

    if request.user.pk in users and (
        question.votes.get(user=request.user).value == value
    ):
        question.votes.get(user=request.user).delete()
    else:
        question.votes.update_or_create(user=request.user,
                                        defaults={'value': value})

    push_notification(
        actor=request.user,
        recipient=question.user,
        verb='L',
        action_object=question
    )
    return JsonResponse({
        'votes': question.total_votes()
    })


@login_required
@ajax_required
@require_POST
def answer_vote(request):
    '''给回答投票'''
    answer_id = request.POST['answer']
    value = True if request.POST['value'] == 'U' else False
    answer = Answer.objects.get(pk=answer_id)
    users = answer.votes.values_list('user', flat=True)


    if request.user.pk in users and (
        answer.votes.get(user=request.user).value == value
    ):
        answer.votes.get(user=request.user).delete()
    else:
        answer.votes.update_or_create(user=request.user,
                                      defaults={'value': value})

    push_notification(
        actor=request.user,
        recipient=answer.user,
        verb='L',
        action_object=answer
    )

    return JsonResponse({
        'votes': answer.total_votes()
    })


@login_required
@ajax_required
@require_POST
def accept_answer(request):
    '''接受回答'''
    answer_id = request.POST['answer']
    answer = Answer.objects.get(pk=answer_id)

    if answer.question.user.username != request.user.username:
        raise PermissionDenied()
    answer.accept_answer()
    #采纳答案后回答者金币+10
    #answer.user.money += Decimal(1)
    push_notification(
        actor=request.user,
        recipient=answer.user,
        verb="W",
        action_object=answer
    )


    return JsonResponse({
        'status': 'true'
    })


class QuestionManageView(LoginRequiredMixin, AuthorRequiredMixin, ListView):
    context_object_name = 'questions'
    template_name = 'qa/question_manage.html'

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(object_list=None, **kwargs)
        context['count'] = self.get_queryset().count()
        return context
