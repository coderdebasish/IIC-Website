"""IIC-IEM – Council Forms"""
from django import forms
from .models import CouncilYear, CouncilMember


class CouncilYearForm(forms.ModelForm):
    class Meta:
        model = CouncilYear
        fields = ['year_label', 'is_current', 'description']
        widgets = {
            'year_label': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '2025-2026'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }


class CouncilMemberForm(forms.ModelForm):
    class Meta:
        model = CouncilMember
        fields = ['council_year', 'name', 'role', 'designation', 'member_type', 'photo', 'email', 'linkedin_url', 'order_no', 'is_active']
        widgets = {
            'council_year': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'role': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'President, Secretary, Faculty Advisor...'}),
            'designation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Branch/Dept, Year (for students)'}),
            'member_type': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-input'}),
            'order_no': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
