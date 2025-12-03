from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from django.db.models import Count

from .models import Course, CoursePart, Comment, CourseRelation, CoursePartProcess


def courses(request):
    courses = Course.objects.all()
    recomended = Course.objects.annotate(num_relations=Count('related_users')).order_by('num_relations')
    page_num = request.GET.get('page', 1)
    courses_paginator = Paginator(courses, 5)
    page_items = courses_paginator.get_page(page_num)
    return render(request, 'courses.html',{
        'courses':courses.order_by('time'),
        'recomended':recomended,
        'page':page_items,
        'page_range':courses_paginator.page_range,
        'pagenum':int(page_num),
        'pagename':'courses'
    })

@login_required(login_url="login", redirect_field_name='next')
def course_part_detail(request, course_part_id):
    context = {}
    course_part = get_object_or_404(CoursePart, id=course_part_id)
    context['course_part'] = course_part
    if request.user.is_authenticated:
        CoursePartProcess.objects.get_or_create(user=request.user, course_part=course_part)
        CourseRelation.objects.get_or_create(course=course_part.course, user=request.user)
        if request.method == "POST":
            text = request.POST.get('text')
            complated = request.POST.get('complated')
            if complated:
                cp_process, created = CoursePartProcess.objects.get_or_create(user=request.user, course_part=course_part)
                cp_process.complated = True
                cp_process.save()
                parts = list(course_part.course.parts.all())
                index = parts.index(course_part)
                if index != len(parts)-1:
                    new = parts[index+1]
                    return redirect('course-part-detail', new.id)
                
            if text:
                Comment.objects.create(author=request.user,course_part=course_part, text=text)
    return render(request, 'course_detail.html', context)