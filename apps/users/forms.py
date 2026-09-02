"""
IIC-IEM Website – Users Forms
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class AdminLoginForm(AuthenticationForm):
    """
    Custom login form for the admin panel.
    """
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your username',
            'autofocus': True,
            'autocomplete': 'username',
        })
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = _(
            'Please enter a correct username and password. '
            'Note that both fields may be case-sensitive.'
        )


class AdminUserCreateForm(UserCreationForm):
    """
    Form for Super Admin to create new Admin accounts.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input'})

    def clean_role(self):
        """Only Super Admin can create Super Admin accounts."""
        return self.cleaned_data['role']


class AdminUserEditForm(forms.ModelForm):
    """
    Form for editing admin user details.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'is_active', 'profile_photo', 'bio']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'bio': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }


class ProfileEditForm(forms.ModelForm):
    """
    Form for admins to edit their own profile.
    """
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'profile_photo', 'bio']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }
