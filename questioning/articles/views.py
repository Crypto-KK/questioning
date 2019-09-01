from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from django_comments.signals import comment_was_posted

from questioning.articles.forms import ArticleForm
from questioning.utils.helpers import AuthorRequiredMixin
from questioning.articles.models import Article


class ArticlesListView(ListView):
    '''文章列表'''
    model = Article
    paginate_by = 10
    context_object_name = 'articles'
    template_name = 'articles/article_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticlesListView, self).get_context_data(
            object_list=None, **kwargs)
        context['popular_tags'] = Article.objects.get_counted_tags()
        return context

    def get_queryset(self):
        return Article.objects.get_published()


class DraftListView(ArticlesListView):
    '''草稿箱列表'''

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user).get_drafts()


class ArticleCreateView(LoginRequiredMixin, CreateView):
    '''发表文章'''
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_create.html'
    message = '文章发表成功！'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArticleCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy('articles:list')


class ArticleDetailView(DetailView):
    '''详情'''
    model = Article
    template_name = 'articles/article_detail.html'

    def get_queryset(self):
        return Article.objects.filter(
            pk=self.kwargs['pk']
        )


class ArticleEditView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    '''用户编辑文章'''
    model = Article
    message = '文章编辑成功'
    template_name = 'articles/article_update.html'
    form_class = ArticleForm

    def form_valid(self, form):
        form.instance = self.request.user
        return super(ArticleEditView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('articles:article', kwargs={'pk': self.kwargs['pk']})


class ArticleDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Article
    context_object_name = 'article'
    template_name = 'articles/article_confirm_delete.html'
    success_url = reverse_lazy('articles:list')


class ArticleManageView(LoginRequiredMixin, AuthorRequiredMixin, ListView):
    context_object_name = 'articles'
    template_name = 'articles/article_manage.html'

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(object_list=None, **kwargs)
        context['count'] = self.get_queryset().count()
        return context
