from django.db import models

from pytube import Playlist
from django.utils import timezone
from users.models import User


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=150)
    muallif = models.CharField(max_length=150)
    thumb = models.ImageField(upload_to='course_thumbs/')
    description = models.TextField()
    playlist_url = models.URLField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    time = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-time"]

    def save(self):
        super().save()
        playlist = Playlist(self.playlist_url)
        for video in playlist.videos:
            title = video.title
            description = video.initial_data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['attributedDescription']['content']
            video_link = video.embed_url
            CoursePart.objects.create(
                course = self,
                title = title,
                description = description,
                video_link = video_link,
                time = timezone.now()
            )
    def __str__(self):
        return self.title

class CoursePart(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='parts'
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    video_link = models.URLField()
    time = models.DateTimeField()
    
    class Meta:
        ordering = ["time"]
        
    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    course_part = models.ForeignKey(
        CoursePart,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.text

class CourseRelation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='related_courses'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='related_users'
    )

class CoursePartProcess(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='completed_parts'
    )
    course_part = models.ForeignKey(
        CoursePart,
        on_delete=models.CASCADE,
        related_name='process'
    )

    complated = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'course_part')

    def __str__(self):
        return f"{self.user.username} completed {self.course_part.title}"