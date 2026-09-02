"""
IIC-IEM Website – Events App Forms
"""
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Event, EventContent, EventStage, EventReport, EventGalleryImage


class EventForm(forms.ModelForm):
    """Form for creating/editing an event's basic information."""
    class Meta:
        model = Event
        fields = [
            'title', 'slug', 'short_description', 'poster',
            'start_date', 'end_date', 'status',
            'registration_link', 'registration_deadline',
            'category', 'tags', 'venue', 'venue_link', 'is_featured',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Event Title'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'auto-generated-from-title'}),
            'short_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Brief description shown on event cards...'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'registration_link': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://forms.google.com/...'}),
            'registration_deadline': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'category': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Workshop, Hackathon, Seminar'}),
            'tags': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'innovation, AI, startup (comma-separated)'}),
            'venue': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Venue name or Online'}),
            'venue_link': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'Google Maps link (optional)'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '').strip()
        if slug:
            from django.utils.text import slugify
            return slugify(slug)
        return slug


class EventContentForm(forms.ModelForm):
    """Form for the rich content editor."""
    class Meta:
        model = EventContent
        fields = ['content']
        widgets = {
            'content': CKEditor5Widget(config_name='default', attrs={'class': 'django_ckeditor_5'}),
        }


class EventStageForm(forms.ModelForm):
    """Form for creating/editing lifecycle stages."""
    class Meta:
        model = EventStage
        fields = ['name', 'description', 'stage_order', 'start_date', 'end_date', 'is_current', 'is_completed']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Registration Open'}),
            'description': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Optional short note'}),
            'stage_order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'start_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class EventReportForm(forms.ModelForm):
    """Form for the event report."""
    class Meta:
        model = EventReport
        fields = ['content', 'pdf_file', 'external_link', 'is_published']
        widgets = {
            'content': CKEditor5Widget(config_name='default', attrs={'class': 'django_ckeditor_5'}),
            'external_link': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://drive.google.com/...'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class EventGalleryImageForm(forms.ModelForm):
    """Form for a single gallery image."""
    class Meta:
        model = EventGalleryImage
        fields = ['image', 'caption', 'order']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Optional caption'}),
            'order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
        }
