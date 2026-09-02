"""IIC-IEM – Announcements Forms"""
from django import forms
from .models import Announcement


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'link', 'link_text', 'priority', 'is_active', 'show_on_home', 'expires_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'link': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'link_text': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Read More'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_on_home': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'expires_at': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
        }
