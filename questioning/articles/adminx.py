from questioning.articles.models import Article

import xadmin


class ArticleAdmin:
    list_display = ['title', 'user','image_data', 'status', 'view_num', 'created_at']
    list_filter = ['title', 'tags', 'created_at']
    search_fields = ['title', 'content']
    ordering = ['-created_at']
    readonly_fields = ['view_num', 'user']

xadmin.site.register(Article, ArticleAdmin)
