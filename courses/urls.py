from django.urls import path

from .views import courses, course_part_detail


urlpatterns = [
    path('', courses, name='courses'),
    path('detail/<int:course_part_id>/', course_part_detail, name='course-part-detail'),
]