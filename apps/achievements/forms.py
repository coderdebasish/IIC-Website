"""IIC-IEM – Achievements Forms"""
from django import forms
from .models import Achievement


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['title', 'description', 'image', 'date', 'category', 'is_featured', 'external_link', 'order_no']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'external_link': forms.URLInput(attrs={'class': 'form-input'}),
            'order_no': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
        }
