from django.urls import path
from django.views.decorators.cache import cache_page
from questioning.articles import views

app_name = 'articles'
urlpatterns = [
    path('', views.ArticlesListView.as_view(), name='list'),
    path('write-new-article/', views.ArticleCreateView.as_view(), name='write_new'),
    path('drafts/', views.DraftListView.as_view(), name='drafts'),
    #path('<int:pk>/', cache_page(60 * 5)(views.ArticleDetailView.as_view()), name='article'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article'),
    path('edit/<int:pk>/', views.ArticleEditView.as_view(), name='edit_article'),
    path('delete/<int:pk>/', views.ArticleDeleteView.as_view(), name='delete_article'),

    path('manage/', views.ArticleManageView.as_view(), name='manage')
]
