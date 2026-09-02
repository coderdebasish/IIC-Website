"""
IIC-IEM Website – Core App Views
Homepage, About, Contact, and Admin Site Settings
"""
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import SiteSettings
from apps.events.models import Event
from apps.achievements.models import Achievement
from apps.announcements.models import Announcement
from apps.users.decorators import admin_required, super_admin_required
from apps.users.utils import log_activity
from apps.users.models import AdminActivityLog
from django.core.cache import cache


# ─── Public Views ──────────────────────────────────────────────────────────────

def homepage(request):
    """Public homepage — aggregates content from all sections."""
    settings_obj = SiteSettings.get_settings()

    # Featured / upcoming events
    upcoming_events = Event.objects.filter(
        status__in=['upcoming', 'ongoing']
    ).order_by('start_date')[:4]

    # Recent past events
    recent_events = Event.objects.filter(
        status='completed'
    ).order_by('-start_date')[:3]

    # Featured achievements
    featured_achievements = Achievement.objects.filter(
        is_featured=True
    ).order_by('-date')[:4]

    # Active homepage announcements
    announcements = Announcement.get_active().filter(
        show_on_home=True
    ).order_by('-created_at')[:5]

    context = {
        'title': f"{settings_obj.site_name} – {settings_obj.tagline}",
        'meta_description': settings_obj.meta_description,
        'upcoming_events': upcoming_events,
        'recent_events': recent_events,
        'featured_achievements': featured_achievements,
        'announcements': announcements,
    }
    return render(request, 'core/homepage.html', context)


def about(request):
    """Public About IIC page."""
    settings_obj = SiteSettings.get_settings()
    context = {
        'title': f'About IIC – {settings_obj.site_name}',
        'meta_description': 'Learn about the Institution\'s Innovation Council (IIC) at IEM Kolkata — our vision, mission, and objectives.',
    }
    return render(request, 'core/about.html', context)


def contact(request):
    """Public Contact & Social page."""
    settings_obj = SiteSettings.get_settings()
    context = {
        'title': f'Contact – {settings_obj.site_name}',
        'meta_description': 'Get in touch with the IIC-IEM team.',
    }
    return render(request, 'core/contact.html', context)


# ─── Admin: Site Settings ──────────────────────────────────────────────────────

@admin_required
def admin_settings(request):
    """Admin panel: General site settings."""
    from .forms import SiteSettingsForm
    settings_obj = SiteSettings.get_settings()
    form = SiteSettingsForm(request.POST or None, request.FILES or None, instance=settings_obj)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # Invalidate cache
            cache.delete('site_settings_singleton')
            log_activity(
                request.user, AdminActivityLog.ActionType.UPDATE,
                'SiteSettings', 1, 'General Settings', request=request
            )
            messages.success(request, 'Site settings updated successfully.')
            return redirect('core:admin_settings')

    return render(request, 'core/admin/settings.html', {
        'title': 'Site Settings',
        'active_tab': 'general',
        'form': form,
    })


@admin_required
def admin_settings_about(request):
    """Admin panel: About/Vision/Mission settings."""
    from .forms import SiteSettingsAboutForm
    settings_obj = SiteSettings.get_settings()
    form = SiteSettingsAboutForm(request.POST or None, instance=settings_obj)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            cache.delete('site_settings_singleton')
            log_activity(
                request.user, AdminActivityLog.ActionType.UPDATE,
                'SiteSettings', 1, 'About/Vision/Mission', request=request
            )
            messages.success(request, 'About content updated successfully.')
            return redirect('core:admin_settings_about')

    return render(request, 'core/admin/settings_about.html', {
        'title': 'About & Mission',
        'active_tab': 'about',
        'form': form,
    })
