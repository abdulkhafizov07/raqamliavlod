from django.contrib import admin

from .models import *


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(CoursePart)
admin.site.register(Comment)
admin.site.register(CourseRelation)
admin.site.register(CoursePartProcess)