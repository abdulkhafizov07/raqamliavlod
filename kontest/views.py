from datetime import timedelta
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Kontest, Masala, UserKontestRelation, UserMasalaRelation
from users.models import User
from .forms import UserMasalaRelationForm
from .decorators import check_contest_time
from django.http import JsonResponse
import json

def kontest(request):
    kontests = Kontest.objects.filter(top=True)
    return render(request, 'kontest.html', {
        'kontests':kontests,
        'pagename':'kontest'
    })

def musobaqalar(request):
    kontests = Kontest.objects.all()
    paginator = Paginator(kontests, 5)
    page_num = request.GET.get('page',1)
    page = paginator.get_page(page_num)
    return render(request, 'musobaqalar.html', {
        'kontests':kontests,
        'pagename':'kontest',
        'page':page,
        'pages':[i for i in range(10-page_num, paginator.num_pages) if abs(page_num-i)<3] if paginator.num_pages>10 else [i for i in range(paginator.num_pages)],
        'total_pages':paginator.num_pages,
    })

def masalalar(request):
    q = request.GET.get("q")
    masalalar = Masala.objects.all()
    if q:
        masalalar = masalalar.filter(title__contains=q)
    else:
        q = ""
    paginator = Paginator(masalalar, 10)
    page_num = request.GET.get('page', 1)
    page = paginator.get_page(page_num)
    return render(request, "masalalar.html", {
        'masalalar':masalalar,
        'pagename':'kontest',
        'page':page,
        'total_pages':paginator.num_pages,
        'pages':paginator.page_range,
        'q':q
    })

MAX_TIME = timedelta(hours=3)
@login_required(login_url="login", redirect_field_name='next')
@check_contest_time
def kontest_detail(request, kontest_id):
    template_name = "kontest_detail.html"
    
    try:
        # Kontestni olish
        kontest = get_object_or_404(Kontest, id=kontest_id)
        
        context = {
            "active_tab": "haqida",
            "kontest": kontest,
            "pagename": "kontest",
            "message": "",
            "warning": "",
            "current_time": timezone.now(),
        }
        
        current_time = timezone.now()
        
        # 1) Foydalanuvchi kontestda qatnashganligini tekshirish
        try:
            user_relation = UserKontestRelation.objects.get(
                kontest=kontest,
                user=request.user
            )
            created = False
        except UserKontestRelation.DoesNotExist:
            # Foydalanuvchi hali qatnashmagan
            user_relation = UserKontestRelation.objects.create(
                kontest=kontest,
                user=request.user,
                created_at=current_time
            )
            created = True
        
        # 2) Agar foydalanuvchi chiqarilgan bo'lsa
        if getattr(user_relation, "is_disqualified", False):
            context["message"] = "error:Siz bu kontestdan chiqarilgansiz va qayta kira olmaysiz!"
            return render(request, template_name, context)
        
        # 3) Kontest tugagan bo'lsa
        if kontest.end_time < current_time:
            context["warning"] = "Yakunlangan!"
            context["tugagan"] = True
            
            # Masalalar ro'yxatini olish
            masalalar = Masala.objects.filter(kontest=kontest, is_published=True)
            context["masalalar"] = masalalar
            
            # Agar masala tanlangan bo'lsa
            masala_id = request.GET.get('masala_id')
            if masala_id:
                try:
                    masala = Masala.objects.get(id=masala_id, kontest=kontest, is_published=True)
                    context["masala"] = masala
                    
                    # Foydalanuvchi yechimlarini olish
                    submissions = UserMasalaRelation.objects.filter(
                        user=request.user,
                        masala=masala
                    ).order_by('-time')[:10]
                    context["submissions"] = submissions
                except Masala.DoesNotExist:
                    pass
                    
            return render(request, template_name, context)
        
        # 4) Kontest hali boshlanmagan bo'lsa
        if kontest.start_time > current_time:
            context["message"] = "info:Kontest hali boshlanmadi. Boshlanish vaqti: " + kontest.start_time.strftime("%d.%m.%Y %H:%M")
            context["kutilmoqda"] = True
            return render(request, template_name, context)
        
        # 5) Kontest davom etmoqda
        context["davom_etmoqda"] = True
        
        # Foydalanuvchi uchun vaqt hisoblash
        if user_relation.created_at:
            # Foydalanuvchi qancha vaqt o'tkazgan
            time_passed = current_time - user_relation.created_at
            time_left = MAX_TIME - time_passed
            
            # Agar vaqti tugagan bo'lsa
            if time_left.total_seconds() <= 0:
                # Foydalanuvchini chiqarib yuborish
                user_relation.is_disqualified = True
                user_relation.disqualified_at = current_time
                user_relation.disqualified_reason = "Vaqt tugadi"
                user_relation.save()
                
                context["message"] = "error:Sizning vaqtingiz tugadi va kontestdan chiqarildingiz!"
                return render(request, template_name, context)
            
            # Qolgan vaqtni hisoblash
            hours = int(time_left.total_seconds() // 3600)
            minutes = int((time_left.total_seconds() % 3600) // 60)
            seconds = int(time_left.total_seconds() % 60)
            
            context["cdown"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            context["cdown_seconds"] = int(time_left.total_seconds())
            
            # Agar 5 daqiqadan kam qolgan bo'lsa, ogohlantirish
            if time_left.total_seconds() < 300:
                context["warning"] = f"Diqqat! Vaqtingiz {minutes} daqiqa {seconds} soniya qoldi!"
        
        else:
            # created_at yo'q bo'lsa, hozirgi vaqtni belgilash
            user_relation.created_at = current_time
            user_relation.save()
            
            hours = int(MAX_TIME.total_seconds() // 3600)
            minutes = int((MAX_TIME.total_seconds() % 3600) // 60)
            seconds = int(MAX_TIME.total_seconds() % 60)
            
            context["cdown"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            context["cdown_seconds"] = int(MAX_TIME.total_seconds())
            
            if created:
                context["message"] = f"success:Sizga {hours} soat vaqt berildi. Vaqtingizdan unumli foydalaning!"
        
        # Masalalar ro'yxatini olish
        masalalar = Masala.objects.filter(kontest=kontest, is_published=True)
        context["masalalar"] = masalalar
        
        # Agar masala tanlangan bo'lsa
        masala_id = request.GET.get('masala_id')
        if masala_id:
            try:
                masala = Masala.objects.get(id=masala_id, kontest=kontest, is_published=True)
                context["masala"] = masala
                
                # Testlarni olish (faqat ko'rsatiladigan testlar)
                tests = Test.objects.filter(masala=masala, hidden=False)
                context["tests"] = tests
                
                # Foydalanuvchi yechimlarini olish
                submissions = UserMasalaRelation.objects.filter(
                    user=request.user,
                    masala=masala
                ).order_by('-time')[:10]
                context["submissions"] = submissions
            except Masala.DoesNotExist:
                pass
        
        # Kontestdagi ishtirokchilar soni
        context["ishtirokchilar_soni"] = UserKontestRelation.objects.filter(
            kontest=kontest, 
            is_disqualified=False
        ).count()
        
        return render(request, template_name, context)
        
    except Exception as e:
        messages.error(request, f"Xatolik yuz berdi: {str(e)}")
        return redirect('kontest')

def kontest_urinishlar(request, kontest_id):
    kontest = get_object_or_404(Kontest, id=kontest_id)
    return render(request, 'kontest_urinishlar.html', {
        'kontest':kontest,
        'pagename':'kontest',
        'active_tab':'urinishlar'
    })

def kontest_masalalar(request, kontest_id):
    kontest = get_object_or_404(Kontest, id=kontest_id)
    return render(request, 'kontest_masalalar.html', {
        'kontest':kontest,
        'pagename':'kontest',
        'active_tab':'masalalar'
    })

def kontest_qatnashuvchilar(request, kontest_id):
    kontest = get_object_or_404(Kontest, id=kontest_id)
    return render(request, 'kontest_qatnashuvchilar.html', {
        'kontest':kontest,
        'pagename':'kontest',
        'active_tab':'qatnashuvchilar'
    })

@csrf_exempt
@login_required(login_url="login", redirect_field_name='next')
@check_contest_time
def masala_detail(request, masala_id):
    language = request.GET.get("language", "C++")
    masala = get_object_or_404(Masala, id=masala_id)
    kontest = get_object_or_404(Kontest, id=masala.kontest.id)

    if masala.kontest:
        if masala.kontest.end_time < timezone.now():
            return HttpResponse("Kontest yakunlangan")

    if request.method == "POST" and request.user.is_authenticated:
        form = UserMasalaRelationForm(request.POST, request.FILES)
        if form.is_valid():
            language = request.POST.get("language", "C++")
            obj:UserMasalaRelation = form.save(commit=False)

            obj.kontetst = masala.kontest
            obj.user = request.user
            obj.masala = masala
            obj.save()

            if obj.state == 'Waiting...':
                obj.get_script_result()
                if obj.state == '🟢 Passed' and UserMasalaRelation.objects.filter(state='🟢 Passed', user=request.user, masala=masala).count()==1 and masala.kontest:
                    kontest_relation = UserKontestRelation.objects.filter(kontest=masala.kontest, user=request.user).first()
                    kontest_relation.score += masala.ball
                    kontest_relation.save()                
        else:
            print(form.errors)
    user_results = UserMasalaRelation.objects.filter(user=request.user, masala=masala)

    time_content = f"<div id=\"timer\">{request.cdown}</div>"

    return render(request, 'masala_detail.html', {
        'masala':masala,
        'kontest':kontest,
        'pagename':'kontest',
        'results':user_results,
        'cdown': request.cdown,
        'user_time_content_html': time_content,
        "language":language
    })

@login_required
@require_POST
def disqualify_user_from_contest(request, contest_id):
    """Admin tomonidan foydalanuvchini kontestdan chiqarish"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Ruxsat yo\'q'}, status=403)
    
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        reason = data.get('reason', 'Sabab kiritilmagan')
        
        user_relation = UserKontestRelation.objects.get(
            kontest_id=contest_id,
            user_id=user_id
        )
        
        user_relation.is_disqualified = True
        user_relation.disqualified_at = timezone.now()
        user_relation.disqualified_reason = reason
        user_relation.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Foydalanuvchi kontestdan chiqarildi'
        })
    except UserKontestRelation.DoesNotExist:
        return JsonResponse({'error': 'Foydalanuvchi topilmadi'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def leave_contest(request, contest_id):
    """Foydalanuvchi o'zi kontestdan chiqish"""
    contest = get_object_or_404(Kontest, id=contest_id)
    
    try:
        user_relation = UserKontestRelation.objects.get(
            kontest=contest,
            user=request.user
        )
        
        # Agar foydalanuvchi allaqachon chiqarilgan bo'lsa
        if user_relation.is_disqualified:
            messages.info(request, "Siz allaqachon kontestdan chiqarilgansiz.")
            kontests = Kontest.objects.filter(top=True)
            return render(request, 'kontest.html', {
                'kontests':kontests,
                'pagename':'kontest'
            })
        
        # Foydalanuvchi o'zi chiqishni tasdiqlashi kerak
        if request.method == 'POST':
            user_relation.is_disqualified = True
            user_relation.disqualified_at = timezone.now()
            user_relation.disqualified_reason = "Foydalanuvchi o'zi chiqdi"
            user_relation.save()
            
            messages.success(request, "Siz kontestdan muvaffaqiyatli chiqdingiz.")
            return redirect('kontest')
        
        # Tasdiqlash sahifasi
        return render(request, 'contest/confirm_leave.html', {
            'contest': contest
        })
        
    except UserKontestRelation.DoesNotExist:
        messages.warning(request, "Siz bu kontestda qatnashmagansiz.")
        return redirect('kontest')
def turnir_jadvali(request, kontest_id):
    kontest = get_object_or_404(Kontest, id=kontest_id)
    # users = User.objects.filter(kontests__kontest_id=kontest_id)
    ratings = UserKontestRelation.objects.filter(kontest=kontest).annotate(
        num_passed=models.Count('user__ishlangan_masalalar', filter=models.Q(user__ishlangan_masalalar__state='🟢 Passed'), distinct=True)
    ).order_by('-score')
    # ratings = users.filter(
    #     ishlangan_masalalar__state='🟢 Passed'
    # ).annotate(
    #     num_passed=models.Count('ishlangan_masalalar', filter=models.Q(ishlangan_masalalar__state='🟢 Passed'), distinct=True),  # Count passed masalalar for each user
    #     total_ball=models.Sum('ishlangan_masalalar__masala__ball', filter=models.Q(ishlangan_masalalar__state='🟢 Passed'), distinct=True)  # Sum of balls for passed masalalar
    # ).order_by("-num_passed")

    return render(request, 'turnir_jadvali.html', {
        'reyting':ratings,
        'kontest':kontest,
        'pagename':'kontest',
        'active_tab':'turnir_jadvali'
    })

#u.ishlangan_masalalar.filter(state__contains="Passed").values("masala").distinct().aggregate(models.Sum("masala__ball"))["masala__ball__sum"]

def reyting(request):
    users = User.objects.filter(
        ishlangan_masalalar__state='🟢 Passed'
    ).annotate(
        num_passed=models.Count('ishlangan_masalalar', filter=models.Q(ishlangan_masalalar__state='🟢 Passed'), distinct=True),  # Count passed masalalar for each user
        total_ball=models.Sum('ishlangan_masalalar__masala__ball', filter=models.Q(ishlangan_masalalar__state='🟢 Passed'), distinct=True)  # Sum of balls for passed masalalar
    )
    users = sorted(users, key=lambda x: -x.get_all_balls())
#    users = User.objects.annotate(
#    total_ball=models.Sum(
#        'ishlangan_masalalar__masala__ball',
#        filter=models.Q(ishlangan_masalalar__state__contains="Passed")
#    ),
#    num_passed=models.Count("ishlangan_masalalar", filter=state__contains="Passed")
#).distinct()
#    users = User.objects.annotate(
#    total_ball=models.Sum(
#        models.F("ishlangan_masalalar__masala__ball"),
#        filter=models.Q(ishlangan_masalalar__state__contains="Passed"),
#        distinct=True
#    )
#).order_by("-total_ball")
    paginator = Paginator(users, 5)
    page_num = request.GET.get('page', 1)
    page = paginator.get_page(page_num)
    start = max(page.number - 5, 1)    
    end = min(start+9, paginator.num_pages)
    start = max(end-9, 1)
    custom_range = range(start, end +1)
    return render(request, 'reyting.html', {
        'pagename':'kontest',
        'reyting':users,
        'page':page,
        'total_pages':list(range(paginator.num_pages)),
        'total_page_count':paginator.num_pages,
        'page_range': custom_range,
        'last_page':paginator.num_pages
    })

def masalalar_ballari(request, k_id):
    kontest = Kontest.objects.get(id=k_id)
    users = sorted(kontest.users.all(), key=lambda x: -sum(x.user.get_kontest_masala_status(k_id)[0][1]))
    users = sorted(users, key=lambda x: (x.user.get_kontest_masala_status(k_id)[0][2], -x.user.get_kontest_masala_status(k_id)[0][3]), reverse=True)

    return render(request, "masalalar_ballari.html", {"kontest":kontest, 'users':users})

def kontestni_tugatish(request, kontest_id):
    kontest = get_object_or_404(Kontest, id=kontest_id)
    for masala in kontest.masalalar.all():
        masala.kontest = None
        masala.save()
    kontest.save()
    return redirect('home')
