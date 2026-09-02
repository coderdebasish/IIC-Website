"""
IIC-IEM Website – Certificates Forms
"""
from django import forms
from .models import Certificate
from apps.events.models import Event


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['certificate_id', 'recipient_name', 'event', 'certificate_type', 'issue_date', 'status', 'notes']
        widgets = {
            'certificate_id': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'IIC-IEM-2026-EVENT-001'}),
            'recipient_name': forms.TextInput(attrs={'class': 'form-input'}),
            'event': forms.Select(attrs={'class': 'form-select'}),
            'certificate_type': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Participant, Winner, Volunteer...'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Internal notes (not shown publicly)'}),
        }

    def clean_certificate_id(self):
        return self.cleaned_data['certificate_id'].strip().upper()


class CertificateImportForm(forms.Form):
    event = forms.ModelChoiceField(
        queryset=Event.objects.order_by('title'),
        required=False,
        label='Associated Event (optional)',
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Select the event these certificates belong to. Can be left blank.',
    )
    file = forms.FileField(
        label='Upload CSV or Excel File',
        widget=forms.FileInput(attrs={'class': 'form-input', 'accept': '.csv,.xlsx,.xls'}),
        help_text='Required columns: certificate_id, recipient_name, certificate_type, issue_date',
    )


class CertificateRevokeForm(forms.Form):
    revocation_reason = forms.CharField(
        label='Reason for Revocation',
        widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Explain why this certificate is being revoked...'}),
        min_length=10,
        help_text='Required. This reason is stored internally and not shown to the public.',
    )
