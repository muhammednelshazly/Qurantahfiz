# apps/accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_STUDENT = 'student'
    ROLE_TEACHER = 'teacher'
    ROLE_CHOICES = (
        (ROLE_STUDENT, 'Student'),
        (ROLE_TEACHER, 'Teacher'),
    )

    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
    )

    # حلقات (10 عناصر)
    HALAQA_CHOICES = (
        ("حلقة البقرة – الشيخ عبد الله الحربي", "حلقة البقرة – الشيخ عبد الله الحربي"),
        ("حلقة النساء – الشيخ محمد القحطاني", "حلقة النساء – الشيخ محمد القحطاني"),
        ("حلقة التوبة – الشيخ خالد الغامدي", "حلقة التوبة – الشيخ خالد الغامدي"),
        ("حلقة النحل – الشيخ فهد العتيبي", "حلقة النحل – الشيخ فهد العتيبي"),
        ("حلقة الإسراء – الشيخ محمود الأنصاري", "حلقة الإسراء – الشيخ محمود الأنصاري"),
        ("حلقة طه – الشيخ علي الزهراني", "حلقة طه – الشيخ علي الزهراني"),
        ("حلقة النمل – الشيخ ياسر البكري", "حلقة النمل – الشيخ ياسر البكري"),
        ("حلقة العنكبوت – الشيخ عبد الرحمن الزهراني", "حلقة العنكبوت – الشيخ عبد الرحمن الزهراني"),
        ("حلقة لقمان – الشيخ إبراهيم السبيعي", "حلقة لقمان – الشيخ إبراهيم السبيعي"),
        ("حلقة فاطر – الشيخ عمر الحربي", "حلقة فاطر – الشيخ عمر الحربي"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_STUDENT)

    # حقول الطالب
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    guardian_phone = models.CharField(max_length=30, null=True, blank=True)
    halaqa = models.CharField(max_length=100, choices=HALAQA_CHOICES, null=True, blank=True)

    # حقول المعلم
    institution = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
