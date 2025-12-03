from django.contrib import admin

# Register your models here.
from .models import ArticleCategory, Article, ArticleRate, ArticleComment


admin.site.register(ArticleCategory)
admin.site.register(Article)
admin.site.register(ArticleRate)
admin.site.register(ArticleComment)