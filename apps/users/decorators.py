"""
IIC-IEM Website – Admin Access Decorators & Mixins
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


def admin_required(view_func):
    """
    Decorator: requires user to be logged in and have at least Admin role.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if not (request.user.is_admin_role or request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to access the admin panel.')
            return redirect('users:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def super_admin_required(view_func):
    """
    Decorator: requires user to be a Super Admin.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if not request.user.is_super_admin:
            messages.error(request, 'This action requires Super Admin privileges.')
            return redirect('users:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


class AdminRequiredMixin(LoginRequiredMixin):
    """
    Class-based view mixin: requires admin role.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if not (request.user.is_admin_role or request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to access the admin panel.')
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)


class SuperAdminRequiredMixin(LoginRequiredMixin):
    """
    Class-based view mixin: requires super admin role.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if not request.user.is_super_admin:
            messages.error(request, 'This action requires Super Admin privileges.')
            return redirect('users:dashboard')
        return super().dispatch(request, *args, **kwargs)
