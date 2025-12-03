from django.urls import path

from .views import articles, article_detail


urlpatterns = [
    path('', articles, name='articles'),
    path('article_detail/<int:article_id>/', article_detail, name='article_detail')
]