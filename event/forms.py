from django import forms
from .models import Event ,Review

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'description',
            'date',
            'time',
            'location',
            'capacity',
        ]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'content'
        ]