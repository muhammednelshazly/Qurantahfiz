from django import forms
from .models import DailyMemorization, Review, Attendance

class DailyMemorizationForm(forms.ModelForm):
    class Meta:
        model = DailyMemorization
        fields = ['student','date','from_surah','from_ayah','to_surah','to_ayah','mastery']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['student','date','surah_or_juz','mastery']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student','date','status']
