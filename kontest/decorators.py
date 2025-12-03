from datetime import timedelta
from django.utils.timezone import now
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from .models import Masala
from functools import wraps
import json
MAX_TIME = timedelta(hours=3)
# print(eval(input().replace(" ", "+")))
# def check_contest_time(fn):
#     def wrapper(request, *args, **kwargs):
#         cdown = "03:00:00"
#         if request.method == "POST":
#             masala = get_object_or_404(Masala, id=kwargs.get('masala_id'))
#             current_time = now()

#             user_contests = request.user.kontests.all()
#             for contest in user_contests:
#                 if masala in contest.kontest.masalalar.all():
#                     if contest.created_at:
#                         time_difference = current_time - contest.created_at
#                         cdown = str(time_difference)
#                         if time_difference > MAX_TIME:
#                             messages.add_message(request, messages.ERROR, "Sizga test yechish uchun berilgan vaqt tugadi.")

#                             return redirect(request.path)
#                     else:
#                         contest.created_at = now()
#                         contest.save()
#                     break

#         return fn(request, cdown=cdown, *args, **kwargs)

#     return wrapper
def check_contest_time(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        kontest_id = kwargs.get('kontest_id') or request.GET.get("kontest_id")
        
        # masala_detail uchun masala_id orqali kontestni olish
        if not kontest_id and "masala_id" in kwargs:
            from kontest.models import Masala
            try:
                masala = Masala.objects.get(id=kwargs["masala_id"])
                kontest_id = masala.kontest.id
            except Masala.DoesNotExist:
                messages.error(request, "Masala topilmadi!")
                return redirect("kontest")

        from kontest.models import Kontest, UserKontestRelation
        try:
            kontest = Kontest.objects.get(id=kontest_id)
        except Kontest.DoesNotExist:
            messages.error(request, "Kontest topilmadi!")
            return redirect("kontest")

        # 1️⃣ Avval foydalanuvchi allaqachon diskval bo'lganmi?
        relation, created = UserKontestRelation.objects.get_or_create(
            kontest=kontest, user=request.user
        )

        if relation.is_disqualified:
            messages.error(request, "Sizning kontest vaqtingiz tugagan yoki siz chiqarilgansiz!")
            return redirect("kontest")

        # 2️⃣ Userning shaxsiy start vaqti
        if not relation.created_at:
            relation.created_at = timezone.now()
            relation.save()
            if created:
                messages.success(request, "Siz kontestga muvaffaqiyatli qo'shildingiz!")

        # 3️⃣ Foydalanuvchi uchun qolgan vaqt
        MAX_TIME = timezone.timedelta(hours=3)  # 3 soat
        time_passed = timezone.now() - relation.created_at
        time_left = MAX_TIME - time_passed

        # 4️⃣ Agar TIME OVER bo'lsa — DISQUALIFY QILAMIZ
        if time_left.total_seconds() <= 0:
            relation.is_disqualified = True
            relation.disqualified_at = timezone.now()
            relation.disqualified_reason = "Vaqti tugadi"
            relation.save()

            messages.error(request, "Sizning shaxsiy kontest vaqtingiz tugadi!")
            return redirect("kontest")

        # 5️⃣ Qolgan vaqtni hisoblash (context uchun)
        total_seconds = int(time_left.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        # Request object'ga qolgan vaqtni qo'shamiz
        request.cdown = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        request.cdown_seconds = total_seconds

        # View funksiyani chaqiramiz
        return view_func(request, *args, **kwargs)

    return wrapper