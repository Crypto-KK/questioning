from django.shortcuts import render
from django.views.generic.list import ListView

from questioning.home.models import Item

class HomeList(ListView):
    template_name = 'home/list.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        return Item.objects.all().order_by('-created_at')
