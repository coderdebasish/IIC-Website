"""IIC-IEM – Gallery Forms"""
from django import forms
from .models import Album


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'cover_image', 'is_published', 'order_no']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'order_no': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
        }
