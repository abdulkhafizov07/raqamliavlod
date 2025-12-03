from django.db import models
from users.models import User
from ckeditor.fields import RichTextField

class ArticleCategory(models.Model):
    title = models.CharField(max_length=150)
    def __str__(self):
        return self.title

class Article(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    title = models.CharField(max_length=150)
    summary = models.CharField(max_length=300)
    image = models.ImageField(upload_to='articles/')
    body = RichTextField()
    accepted = models.BooleanField(default=False)
    time = models.DateField()

    class Meta:
        ordering = ["-time"]

    def __str__(self):
        return self.title

class ArticleView(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='views'
    )

class ArticleRate(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='rates'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rates'
    )
    rate = models.IntegerField()

class ArticleComment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='article_comments'
    )
    text = models.CharField(max_length=200)
    time=models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ["-time"]
    def __str__(self):
        return self.text

