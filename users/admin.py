from django.contrib import admin

# Register your models here.
from .models import User, Profile, DailyActivity

class UserAdmin(admin.ModelAdmin):
    model = User
    search_fields = ['username','first_name', 'last_name', 'email','telefon']

admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_streak', 'longest_streak', 'last_active_date')

@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_date')
    list_filter = ('activity_date',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    date_hierarchy = 'activity_date'
    ordering = ('-activity_date',)
    list_per_page = 20