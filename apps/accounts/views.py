# apps/accounts/views.py
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Profile

def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        role = request.POST.get("role", "")                     # 'student' أو 'teacher'
        remember_me = request.POST.get("remember-me")           # on/None

        if not identifier or not password or role not in (Profile.ROLE_STUDENT, Profile.ROLE_TEACHER):
            messages.error(request, "من فضلك أكمل كل الحقول واختر نوع الحساب (طالب/معلم).")
            return render(request, "accounts/login.html", {"selected_role": role})

        username = identifier
        if "@" in identifier:
            user_obj = User.objects.filter(email__iexact=identifier).first()
            username = user_obj.username if user_obj else None

        user = authenticate(request, username=username, password=password) if username else None
        if user is None:
            messages.error(request, "بيانات الدخول غير صحيحة.")
            return render(request, "accounts/login.html", {"selected_role": role})

        if user.is_staff or user.is_superuser:
            messages.error(request, "لا يُسمح للمشرف/الآدمن بتسجيل الدخول من هذه الصفحة.")
            return render(request, "accounts/login.html", {"selected_role": role})

        if not hasattr(user, "profile"):
            Profile.objects.create(user=user)

        if user.profile.role != role:
            messages.error(request, "نوع الحساب لا يطابق الاختيار (طالب/معلم).")
            return render(request, "accounts/login.html", {"selected_role": role})

        login(request, user)
        if not remember_me:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(14 * 24 * 3600)

        messages.success(request, "تم تسجيل الدخول بنجاح.")
        return redirect("home")

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "تم تسجيل الخروج.")
    return redirect("accounts:login")

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email    = request.POST.get("email", "").strip().lower()
        pw1      = request.POST.get("password1", "")
        pw2      = request.POST.get("password2", "")
        role     = request.POST.get("role", "")

        # حقول الطالب
        birth_date_str  = request.POST.get("birth_date", "").strip()
        gender          = request.POST.get("gender") or None
        guardian_phone  = request.POST.get("guardian_phone") or None
        halaqa          = request.POST.get("halaqa") or None

        # حقول المعلم
        institution     = request.POST.get("institution") or None
        bio             = request.POST.get("bio") or None
        certificate     = request.FILES.get("certificate")  # ملف مرفق اختياري

        # تحققات أساسية
        if not all([username, email, pw1, pw2, role]):
            messages.error(request, "من فضلك أكمل جميع الحقول الأساسية.")
            return render(request, "accounts/register.html", {"selected_role": role})

        if role not in (Profile.ROLE_STUDENT, Profile.ROLE_TEACHER):
            messages.error(request, "برجاء اختيار نوع حساب صحيح (طالب/معلم).")
            return render(request, "accounts/register.html", {"selected_role": role})

        if pw1 != pw2:
            messages.error(request, "كلمتا المرور غير متطابقتين.")
            return render(request, "accounts/register.html", {"selected_role": role})

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "اسم المستخدم مستخدم من قبل.")
            return render(request, "accounts/register.html", {"selected_role": role})

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "البريد الإلكتروني مسجل من قبل.")
            return render(request, "accounts/register.html", {"selected_role": role})

        # تحققات مرتبطة بالدور
        birth_date = None
        if role == Profile.ROLE_STUDENT:
            # الطالب: تاريخ ميلاد + جنس مطلوبين
            if not birth_date_str or not gender:
                messages.error(request, "تاريخ الميلاد والجنس مطلوبان للطالب.")
                return render(request, "accounts/register.html", {"selected_role": role})
            try:
                # نقبل YYYY-MM-DD من input type=date
                birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "صيغة تاريخ الميلاد غير صحيحة.")
                return render(request, "accounts/register.html", {"selected_role": role})

        # إنشاء المستخدم
        user = User.objects.create_user(username=username, email=email, password=pw1)

        # إنشاء/تحديث البروفايل
        if hasattr(user, "profile"):
            profile = user.profile
        else:
            profile = Profile(user=user)

        profile.role = role

        if role == Profile.ROLE_STUDENT:
            profile.birth_date = birth_date
            profile.gender = gender
            profile.guardian_phone = guardian_phone
            profile.halaqa = halaqa
            # حقول المعلم تُترك فارغة
            profile.institution = None
            profile.bio = None
            if profile.certificate:
                profile.certificate.delete(save=False)
            profile.certificate = None
        else:
            # معلم
            profile.institution = institution
            profile.bio = bio
            if certificate:
                profile.certificate = certificate
            # حقول الطالب اختيارية/فارغة
            profile.birth_date = None
            profile.gender = None
            profile.guardian_phone = None
            profile.halaqa = None

        profile.save()

        messages.success(request, "تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن.")
        return redirect("accounts:login")

    return render(request, "accounts/register.html")

@login_required(login_url="accounts:login")
def home_view(request):
    return render(request, "home.html")
