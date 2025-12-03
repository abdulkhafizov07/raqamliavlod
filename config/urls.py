from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('telegram/', include('telegram_bot.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('courses/', include('courses.urls')),
    path('articles/', include('articles.urls')),
    path('forum/', include('forum.urls')),
    path('kontest/', include('kontest.urls')),
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)