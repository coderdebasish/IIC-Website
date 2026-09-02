"""
IIC-IEM Website – Users Views (Admin Panel: Auth + User Management)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import CustomUser, AdminActivityLog
from .forms import AdminLoginForm, AdminUserCreateForm, AdminUserEditForm, ProfileEditForm
from .decorators import admin_required, super_admin_required
from .utils import log_activity

# ─── Authentication ────────────────────────────────────────────────────────────

def admin_login(request):
    """Admin panel login view."""
    if request.user.is_authenticated and request.user.is_admin_role:
        return redirect('users:dashboard')

    form = AdminLoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if not user.is_admin_role:
                messages.error(request, 'You do not have admin access.')
                return render(request, 'users/login.html', {'form': form})

            login(request, user)

            # Track login IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
            user.last_login_ip = ip
            user.save(update_fields=['last_login_ip'])

            log_activity(user, AdminActivityLog.ActionType.LOGIN, 'CustomUser', user.pk, str(user), request=request)
            messages.success(request, f'Welcome back, {user.get_display_name()}!')
            next_url = request.GET.get('next', 'users:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'users/login.html', {'form': form, 'title': 'Admin Login'})


@require_POST
@admin_required
def admin_logout(request):
    """Admin panel logout."""
    log_activity(request.user, AdminActivityLog.ActionType.LOGOUT, 'CustomUser', request.user.pk, str(request.user), request=request)
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('users:login')


# ─── Dashboard ─────────────────────────────────────────────────────────────────

@admin_required
def dashboard(request):
    """Main admin dashboard with summary stats."""
    from apps.events.models import Event
    from apps.certificates.models import Certificate
    from apps.announcements.models import Announcement

    # Summary stats
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(status='upcoming').count()
    total_certificates = Certificate.objects.count()
    active_announcements = Announcement.objects.filter(is_active=True).count()

    # Recent activity
    recent_logs = AdminActivityLog.objects.select_related('admin_user').order_by('-created_at')[:10]

    # Recent events
    recent_events = Event.objects.order_by('-created_at')[:5]

    context = {
        'title': 'Dashboard',
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'total_certificates': total_certificates,
        'active_announcements': active_announcements,
        'recent_logs': recent_logs,
        'recent_events': recent_events,
    }
    return render(request, 'users/dashboard.html', context)


# ─── Admin Profile ─────────────────────────────────────────────────────────────

@admin_required
def profile(request):
    """Admin user's own profile page."""
    form = ProfileEditForm(request.POST or None, request.FILES or None, instance=request.user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            log_activity(request.user, AdminActivityLog.ActionType.UPDATE, 'CustomUser', request.user.pk, 'Profile updated', request=request)
            messages.success(request, 'Profile updated successfully.')
            return redirect('users:profile')

    return render(request, 'users/profile.html', {'form': form, 'title': 'My Profile'})


@admin_required
def change_password(request):
    """Password change view."""
    form = PasswordChangeForm(user=request.user, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep session alive
            log_activity(request.user, AdminActivityLog.ActionType.UPDATE, 'CustomUser', request.user.pk, 'Password changed', request=request)
            messages.success(request, 'Password changed successfully.')
            return redirect('users:profile')

    return render(request, 'users/change_password.html', {'form': form, 'title': 'Change Password'})


# ─── Admin User Management (Super Admin Only) ───────────────────────────────────

@super_admin_required
def user_list(request):
    """List all admin users. Super Admin only."""
    search = request.GET.get('q', '').strip()
    users = CustomUser.objects.exclude(pk=request.user.pk)

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )

    context = {
        'title': 'Manage Admin Users',
        'users': users.order_by('username'),
        'search': search,
    }
    return render(request, 'users/user_list.html', context)


@super_admin_required
def user_create(request):
    """Create a new admin user. Super Admin only."""
    form = AdminUserCreateForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_staff = True  # Allow Django admin access
            new_user.save()
            log_activity(request.user, AdminActivityLog.ActionType.CREATE, 'CustomUser', new_user.pk, str(new_user), f'Role: {new_user.role}', request=request)
            messages.success(request, f'Admin user "{new_user.username}" created successfully.')
            return redirect('users:user_list')

    return render(request, 'users/user_form.html', {'form': form, 'title': 'Create Admin User', 'action': 'Create'})


@super_admin_required
def user_edit(request, pk):
    """Edit an admin user. Super Admin only."""
    user_obj = get_object_or_404(CustomUser, pk=pk)

    # Prevent editing own account through this view (use profile instead)
    if user_obj.pk == request.user.pk:
        messages.info(request, 'To edit your own account, use the Profile page.')
        return redirect('users:profile')

    form = AdminUserEditForm(request.POST or None, request.FILES or None, instance=user_obj)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            log_activity(request.user, AdminActivityLog.ActionType.UPDATE, 'CustomUser', user_obj.pk, str(user_obj), request=request)
            messages.success(request, f'User "{user_obj.username}" updated successfully.')
            return redirect('users:user_list')

    return render(request, 'users/user_form.html', {
        'form': form,
        'title': f'Edit User: {user_obj.username}',
        'action': 'Save Changes',
        'user_obj': user_obj,
    })


@super_admin_required
@require_POST
def user_toggle_active(request, pk):
    """Enable/disable an admin user. Super Admin only."""
    user_obj = get_object_or_404(CustomUser, pk=pk)

    if user_obj.pk == request.user.pk:
        messages.error(request, 'You cannot disable your own account.')
        return redirect('users:user_list')

    user_obj.is_active = not user_obj.is_active
    user_obj.save(update_fields=['is_active'])

    action_word = 'enabled' if user_obj.is_active else 'disabled'
    log_activity(
        request.user,
        AdminActivityLog.ActionType.UPDATE,
        'CustomUser', user_obj.pk, str(user_obj),
        f'Account {action_word}',
        request=request,
    )
    messages.success(request, f'User "{user_obj.username}" has been {action_word}.')
    return redirect('users:user_list')


@super_admin_required
def activity_log(request):
    """View admin activity log. Super Admin only."""
    logs = AdminActivityLog.objects.select_related('admin_user').order_by('-created_at')[:200]
    return render(request, 'users/activity_log.html', {
        'title': 'Activity Log',
        'logs': logs,
    })
