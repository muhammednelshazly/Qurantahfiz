# apps/accounts/admin.py
from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'gender', 'halaqa', 'institution')
    list_select_related = ('user',)
    list_filter = ('role', 'gender', 'halaqa')
    search_fields = ('user__username', 'user__email', 'institution')
    fieldsets = (
        ('الأساسي', {
            'fields': ('user', 'role')
        }),
        ('بيانات الطالب', {
            'fields': ('birth_date', 'gender', 'guardian_phone', 'halaqa'),
            'classes': ('collapse',)
        }),
        ('بيانات المعلم', {
            'fields': ('institution', 'bio', 'certificate'),
            'classes': ('collapse',)
        }),
    )
