from django.db import models

from ckeditor.fields import RichTextField

from users.models import User


class Question(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='forum_questions',
    )
    title = models.CharField(max_length=150)
    body = RichTextField()
    time = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-time"]
        
    def __str__(self):
        return self.title

class Answer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    text = RichTextField()
    time = models.DateField(auto_now_add=True)
    class Meta:
        ordering = ["-time"]
        
    def __str__(self):
        return self.text

class ForumView(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='views'
    )

class ForumLike(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='likes'
    )
