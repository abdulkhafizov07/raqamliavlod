from django.shortcuts import render, get_object_or_404, redirect

from django.db.models import Avg
from users.models import User
from .models import ArticleCategory, Article, ArticleView, ArticleRate, ArticleComment
from .forms import ArticleForm

def articles(request):
    if request.method == "POST" and request.user.is_authenticated:
        print(request.POST)
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()        
    else:
        form = ArticleForm()
    articles = Article.objects.all()
    article_categories = ArticleCategory.objects.all()
    return render(request, 'articles.html', {
        'articles':articles,
        'pagename':'articles',
        'article_categories':article_categories,
        'form':form
    })

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    ArticleView.objects.create(article=article)

    rate = request.GET.get('rate',0)
    if rate and request.user.is_authenticated:
        if not ArticleRate.objects.filter(article=article, user=request.user).exists():
            ArticleRate.objects.create(article=article, user=request.user, rate=rate)
            return redirect('article_detail', article_id=article_id)
    if request.method == "POST" and request.user.is_authenticated:
        comment = request.POST.get('comment')
        if comment:
            ArticleComment.objects.create(article=article, user=request.user, text=comment)
            return redirect('article_detail', article_id=article_id)
    mean_rate = article.rates.aggregate(Avg('rate'))['rate__avg']
    user_login = False
    if User.is_authenticated:
        user_login = True
    else:
        user_login = False
    return render(request, 'article_detail.html', {
        'user_login':user_login,
        'article':article,
        'mean_rate':mean_rate,
        'pagename':'articles',
        'related':Article.objects.filter(category=article.category).order_by('?')[:5],
    })


