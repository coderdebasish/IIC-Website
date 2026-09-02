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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure default academic years exist if database is empty
        if not CouncilYear.objects.exists():
            CouncilYear.objects.get_or_create(year_label='2025-2026', defaults={'is_current': True, 'description': 'Academic Session 2025-2026'})
            CouncilYear.objects.get_or_create(year_label='2024-2025', defaults={'is_current': False, 'description': 'Academic Session 2024-2025'})
            CouncilYear.objects.get_or_create(year_label='2023-2024', defaults={'is_current': False, 'description': 'Academic Session 2023-2024'})
        
        self.fields['council_year'].queryset = CouncilYear.objects.order_by('-year_label')
        
        # Set default initial selection to current academic year for new member forms
        if not self.instance.pk and 'council_year' in self.fields:
            current_yr = CouncilYear.objects.filter(is_current=True).first() or CouncilYear.objects.first()
            if current_yr:
                self.fields['council_year'].initial = current_yr.pk

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
