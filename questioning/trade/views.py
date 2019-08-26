from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View, TemplateView

from questioning.utils.helpers import AuthorRequiredMixin


class DepositView(LoginRequiredMixin, AuthorRequiredMixin, TemplateView):
    template_name = 'trade/deposit.html'
