from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='news/')
    time = models.DateTimeField()
    tg_url = models.CharField(max_length=1000)
    class Meta:
        ordering = ["-time"]
        
    def __str__(self):
        return self.title
