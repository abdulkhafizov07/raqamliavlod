from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    #class Meta:
        #ordering = [models.F('kontests__masalalar__ishlanganlar__state')]
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            'unique': 'Bu foydalanuvchi nomi band. Iltimos, boshqa nom kiriting.',
        }
    )
    profile_image = models.ImageField(upload_to="pfiles/", null=True, blank=True)
    telefon = models.CharField(max_length=20, default="Kiritilmagan")
    telegram = models.CharField(max_length=150, default="Kiritilmagan")
    viloyat = models.CharField(max_length=100, default="Kiritilmagan")
    tuman = models.CharField(max_length=100, default="Kiritilmagan")
    maktab = models.CharField(max_length=300, default="Kiritilmagan")
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_all_balls(self):
        res = self.ishlangan_masalalar.filter(state='🟢 Passed').aggregate(models.Sum('masala__ball', distinct=True))['masala__ball__sum']
        # self.ishlangan_masalalar.filter(state='🟢 Passed').annotate(sum_ball=Sum('masala__ball')).first()
        res = self.ishlangan_masalalar.filter(state__contains="Passed").values("masala").distinct().aggregate(models.Sum("masala__ball"))["masala__ball__sum"]
        return res if res else 0
    
    def get_kontest_masala_status(self, k_id=None):
        result = []
        kontests = self.kontests.all()
        for k in kontests:
            if k_id:
                if k_id != k.kontest.id:
                    continue
            k_masalalar_ball = []
            k_masalalar_time = []
            k_urinishlar_soni = 0
            k_masalalar = k.kontest.masalalar.all()
            urinish_start = None
            urinish_end = None
            for m in k_masalalar:
                if urinish_start == None:
                    urinish_start = m.ishlaganlar.filter(user=self).first()
                ball = 0
                try:
                    ball = m.ishlaganlar.filter(user=self,state="🟢 Passed").order_by("time").first().masala.ball
                except:
                    pass
                k_masalalar_ball.append(ball)
                k_masalalar_time.append(m.ishlaganlar.filter(user=self,state="🟢 Passed").order_by("time").first().time if ball else '0')
                k_urinishlar_soni += m.ishlaganlar.filter(user=self).count()
                urinish_end = urinish_end

            result.append((k.kontest.id,k_masalalar_ball, len(k_masalalar_ball)-k_masalalar_ball.count(0),k_urinishlar_soni,k_masalalar_time))
        return result
    
    def course_process(self, course_id):
        course = self.related_courses.get(course__id=course_id)
        complated_parts = self.completed_parts(course_part__course_id=course_id, complated=True).count()
        course_parts = course.parts.count()
        return int(complated_parts/(course_parts/100))

class DailyActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_activities')
    activity_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'activity_date') 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_active_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
