"""IIC-IEM – Achievements Views"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from apps.users.decorators import admin_required
from apps.users.utils import log_activity
from apps.users.models import AdminActivityLog
from .models import Achievement
from .forms import AchievementForm


def achievement_list(request):
    category_filter = request.GET.get('category', '')
    achievements = Achievement.objects.order_by('-date', '-created_at')
    if category_filter:
        achievements = achievements.filter(category=category_filter)
    return render(request, 'achievements/achievement_list.html', {
        'title': 'Achievements – IIC IEM',
        'meta_description': 'Awards, recognitions, and milestones achieved by the IIC at IEM Kolkata.',
        'achievements': achievements,
        'category_choices': Achievement.Category.choices,
        'active_category': category_filter,
    })


@admin_required
def admin_achievement_list(request):
    achievements = Achievement.objects.order_by('-date', '-created_at')
    return render(request, 'achievements/admin/achievement_list.html', {'title': 'Manage Achievements', 'achievements': achievements})


@admin_required
def admin_achievement_add(request):
    form = AchievementForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        ach = form.save()
        log_activity(request.user, AdminActivityLog.ActionType.CREATE, 'Achievement', ach.pk, ach.title, request=request)
        messages.success(request, f'Achievement "{ach.title}" added.')
        return redirect('achievements:admin_list')
    return render(request, 'achievements/admin/achievement_form.html', {'title': 'Add Achievement', 'form': form, 'action': 'Add'})


@admin_required
def admin_achievement_edit(request, pk):
    ach = get_object_or_404(Achievement, pk=pk)
    form = AchievementForm(request.POST or None, request.FILES or None, instance=ach)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Achievement "{ach.title}" updated.')
        return redirect('achievements:admin_list')
    return render(request, 'achievements/admin/achievement_form.html', {'title': f'Edit: {ach.title}', 'form': form, 'achievement': ach, 'action': 'Save'})


@admin_required
@require_POST
def admin_achievement_delete(request, pk):
    ach = get_object_or_404(Achievement, pk=pk)
    title = ach.title
    log_activity(request.user, AdminActivityLog.ActionType.DELETE, 'Achievement', ach.pk, title, request=request)
    ach.delete()
    messages.success(request, f'Achievement "{title}" deleted.')
    return redirect('achievements:admin_list')
