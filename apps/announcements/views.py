"""IIC-IEM – Announcements Views"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from apps.users.decorators import admin_required
from apps.users.utils import log_activity
from apps.users.models import AdminActivityLog
from .models import Announcement
from .forms import AnnouncementForm


def announcement_list(request):
    announcements = Announcement.get_active().order_by('-created_at')
    return render(request, 'announcements/announcement_list.html', {
        'title': 'Announcements – IIC IEM',
        'announcements': announcements,
    })


@admin_required
def admin_announcement_list(request):
    announcements = Announcement.objects.order_by('-created_at')
    return render(request, 'announcements/admin/announcement_list.html', {'title': 'Manage Announcements', 'announcements': announcements})


@admin_required
def admin_announcement_add(request):
    form = AnnouncementForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        ann = form.save()
        log_activity(request.user, AdminActivityLog.ActionType.CREATE, 'Announcement', ann.pk, ann.title, request=request)
        messages.success(request, f'Announcement "{ann.title}" published.')
        return redirect('announcements:admin_list')
    return render(request, 'announcements/admin/announcement_form.html', {'title': 'Add Announcement', 'form': form, 'action': 'Publish'})


@admin_required
def admin_announcement_edit(request, pk):
    ann = get_object_or_404(Announcement, pk=pk)
    form = AnnouncementForm(request.POST or None, instance=ann)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Announcement "{ann.title}" updated.')
        return redirect('announcements:admin_list')
    return render(request, 'announcements/admin/announcement_form.html', {'title': f'Edit: {ann.title}', 'form': form, 'announcement': ann, 'action': 'Save'})


@admin_required
@require_POST
def admin_announcement_toggle(request, pk):
    ann = get_object_or_404(Announcement, pk=pk)
    ann.is_active = not ann.is_active
    ann.save(update_fields=['is_active'])
    state = 'published' if ann.is_active else 'unpublished'
    log_activity(request.user, AdminActivityLog.ActionType.PUBLISH if ann.is_active else AdminActivityLog.ActionType.UNPUBLISH, 'Announcement', ann.pk, ann.title, request=request)
    messages.success(request, f'Announcement "{ann.title}" {state}.')
    return redirect('announcements:admin_list')


@admin_required
@require_POST
def admin_announcement_delete(request, pk):
    ann = get_object_or_404(Announcement, pk=pk)
    title = ann.title
    ann.delete()
    messages.success(request, f'Announcement "{title}" deleted.')
    return redirect('announcements:admin_list')
