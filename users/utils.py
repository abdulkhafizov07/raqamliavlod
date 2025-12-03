# utils.py
from datetime import timedelta, date
from .models import DailyActivity

def update_user_streak(user):
    today = date.today()
    yesterday = today - timedelta(days=1)

    # Get all unique activity dates for this user (sorted DESC)
    dates = DailyActivity.objects.filter(user=user).values_list('activity_date', flat=True).order_by('-activity_date').distinct()

    streak = 0
    for i, activity_date in enumerate(dates):
        if i == 0:
            if activity_date == today or activity_date == yesterday:
                streak += 1
                last_date = activity_date
            else:
                break
        else:
            if (last_date - activity_date).days == 1:
                streak += 1
                last_date = activity_date
            else:
                break

    # Update the user's profile
    profile = user.profile
    profile.last_active_date = dates[0] if dates else None
    profile.current_streak = streak
    profile.longest_streak = max(profile.longest_streak, streak)
    profile.save()
