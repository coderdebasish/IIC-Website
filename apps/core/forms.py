"""
IIC-IEM Website – Core App Forms
"""
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    """General site settings form."""
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'tagline', 'logo', 'favicon',
            'hero_tagline', 'hero_description', 'hero_background',
            'president_name', 'president_designation', 'president_message', 'president_image',
            'stat_1_number', 'stat_1_label', 'stat_2_number', 'stat_2_label',
            'stat_3_number', 'stat_3_label', 'stat_4_number', 'stat_4_label',
            'contact_email', 'contact_phone', 'contact_address',
            'facebook_url', 'instagram_url', 'twitter_url', 'linkedin_url', 'youtube_url',
            'footer_text', 'meta_description', 'meta_keywords',
        ]
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-input'}),
            'tagline': forms.TextInput(attrs={'class': 'form-input'}),
            'hero_tagline': forms.TextInput(attrs={'class': 'form-input'}),
            'hero_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'president_name': forms.TextInput(attrs={'class': 'form-input'}),
            'president_designation': forms.TextInput(attrs={'class': 'form-input'}),
            'president_message': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'stat_1_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '120+'}),
            'stat_1_label': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Innovation Workshops & Hackathons'}),
            'stat_2_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '45+'}),
            'stat_2_label': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Student Startups Mentored'}),
            'stat_3_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '30+'}),
            'stat_3_label': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Patents & Copyrights Filed'}),
            'stat_4_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '₹2.5 Cr+'}),
            'stat_4_label': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Grant Exposure & Funding Support'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-input'}),
            'contact_address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://facebook.com/...'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://instagram.com/...'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://x.com/...'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://linkedin.com/...'}),
            'youtube_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://youtube.com/...'}),
            'footer_text': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'meta_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'maxlength': 300}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-input'}),
        }


class SiteSettingsAboutForm(forms.ModelForm):
    """About / Vision / Mission settings form."""
    class Meta:
        model = SiteSettings
        fields = ['about_iic', 'about_iic_at_iem', 'vision', 'mission', 'objectives']
        widgets = {
            'about_iic': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 8}),
            'about_iic_at_iem': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 8}),
            'vision': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'mission': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'objectives': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 8}),
        }
