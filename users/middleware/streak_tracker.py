# middleware/streak_tracker.py
from datetime import date
from django.utils.deprecation import MiddlewareMixin
from users.models import DailyActivity
from users.utils import update_user_streak

class StreakTrackerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            today = date.today()

            # Create activity log only once per day
            activity, created = DailyActivity.objects.get_or_create(
                user=request.user,
                activity_date=today
            )
            

            # If it's a new activity for today, update the streak
            if created:
                update_user_streak(request.user)
