from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Question
from .forms import QuestionForm, AnswerForm


def forums(request):
    forums = Question.objects.all()
    return render(request, 'forum.html', {
        'forums':forums,
        'pagename':'forum'
    })

@login_required(login_url='login', redirect_field_name='next')
def forum_create(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('forum')
        else:
            print(form.errors)
    else:
        form = QuestionForm()

    return render(request, 'forum_create.html', {
        'form':form,
        'pagename':'forum'
    })

def forum_detail(request, forum_id):
    forum = get_object_or_404(Question, id=forum_id)
    if request.method == "POST" and request.user.is_authenticated:
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            print(19)
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = forum
            answer.save()
            return redirect('forum-detail', forum_id=forum_id)
    else:
        form = AnswerForm()
    return render(request, 'forum_detail.html', {
        'forum':forum,
        'form':form,
        'pagename':'forum'
    })