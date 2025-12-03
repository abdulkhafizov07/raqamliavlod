from django.urls import path

from .views import forums, forum_detail,forum_create


urlpatterns = [
    path('', forums, name='forum'),
    path('create/', forum_create, name='forum-create'),
    path('detail/<int:forum_id>/', forum_detail, name='forum-detail')
]