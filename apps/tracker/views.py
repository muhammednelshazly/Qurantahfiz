from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg, Count, Q
from datetime import date, timedelta
from .models import Student, DailyMemorization, Review, Attendance, Halaqa
from .forms import DailyMemorizationForm, ReviewForm, AttendanceForm

@login_required
def student_dashboard(request):
    student = getattr(request.user, 'student_profile', None)
    if not student:
        messages.error(request, "Student profile not found.")
        return redirect('home')

    memos_qs      = DailyMemorization.objects.filter(student=student).order_by('-date')
    reviews_qs    = Review.objects.filter(student=student).order_by('-date')
    attendance_qs = Attendance.objects.filter(student=student).order_by('-date')

    memos      = memos_qs[:5]
    reviews    = reviews_qs[:10]
    attendance = attendance_qs[:10]

    mastery_avg = memos_qs.aggregate(avg=Avg('mastery'))['avg'] or 0

    total = attendance_qs.count()
    if total:
        present = attendance_qs.filter(status='present').count()
        attendance_rate = present / total * 100
    else:
        attendance_rate = 0

    return render(request, 'dashboard/student_dashboard.html', {
        'student': student,
        'memos': memos,
        'reviews': reviews,
        'attendance': attendance,
        'mastery_avg': round(mastery_avg, 1),
        'attendance_rate': round(attendance_rate, 1),
    })

@login_required
def teacher_dashboard(request):
    halaqat = Halaqa.objects.filter(teacher=request.user).prefetch_related('students')
    recent = DailyMemorization.objects.filter(student__halaqa__teacher=request.user)[:10]
    return render(request, 'dashboard/teacher_dashboard.html', {'halaqat': halaqat, 'recent': recent})

@login_required
def admin_dashboard(request):
    # Simple KPIs
    students_count = Student.objects.count()
    total_memos = DailyMemorization.objects.count()
    present_count = Attendance.objects.filter(status='present').count()
    absent_count = Attendance.objects.filter(status='absent').count()
    return render(request, 'dashboard/admin_dashboard.html', {
        'students_count': students_count,
        'total_memos': total_memos,
        'present_count': present_count,
        'absent_count': absent_count,
    })

@login_required
def record_memorization(request):
    if request.method == 'POST':
        form = DailyMemorizationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Memorization saved.")
            return redirect('tracker:teacher_dashboard')
    else:
        form = DailyMemorizationForm()
    return render(request, 'forms/record_form.html', {'form': form, 'title': 'Record Memorization'})

@login_required
def record_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Review saved.")
            return redirect('tracker:teacher_dashboard')
    else:
        form = ReviewForm()
    return render(request, 'forms/record_form.html', {'form': form, 'title': 'Record Review'})

@login_required
def record_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance saved.")
            return redirect('tracker:teacher_dashboard')
    else:
        form = AttendanceForm()
    return render(request, 'forms/record_form.html', {'form': form, 'title': 'Record Attendance'})
