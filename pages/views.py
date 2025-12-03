from django.shortcuts import render
from news.models import News
from courses.models import Course
from users.models import Profile

def home(request):
    if request.user.is_authenticated:
        Profile.objects.get_or_create(user=request.user)
    news = News.objects.all()
    courses = Course.objects.all()
    return render(request, 'home.html', {
        'news':news,
        'courses':courses,
        'pagename':'home'
    })