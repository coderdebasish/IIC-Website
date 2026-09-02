"""IIC-IEM – Council, Achievements, Gallery, Announcements Views (stub + full)"""
# council/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from apps.users.decorators import admin_required
from apps.users.utils import log_activity
from apps.users.models import AdminActivityLog
from .models import CouncilYear, CouncilMember
from .forms import CouncilYearForm, CouncilMemberForm


def council_current(request):
    try:
        year = CouncilYear.objects.get(is_current=True)
    except CouncilYear.DoesNotExist:
        year = CouncilYear.objects.order_by('-year_label').first()

    all_years = CouncilYear.objects.order_by('-year_label')
    members = CouncilMember.objects.filter(council_year=year).order_by('member_type', 'order_no') if year else []
    faculty = [m for m in members if m.member_type == 'faculty']
    students = [m for m in members if m.member_type == 'student']

    return render(request, 'council/council.html', {
        'title': 'Council Members – IIC IEM',
        'meta_description': 'Meet the faculty and student members of the Institution\'s Innovation Council at IEM Kolkata.',
        'current_year': year,
        'all_years': all_years,
        'faculty_members': faculty,
        'student_members': students,
    })


def council_by_year(request, year_label):
    year = get_object_or_404(CouncilYear, year_label=year_label)
    all_years = CouncilYear.objects.order_by('-year_label')
    members = CouncilMember.objects.filter(council_year=year).order_by('member_type', 'order_no')
    faculty = [m for m in members if m.member_type == 'faculty']
    students = [m for m in members if m.member_type == 'student']

    return render(request, 'council/council.html', {
        'title': f'Council {year.year_label} – IIC IEM',
        'current_year': year,
        'all_years': all_years,
        'faculty_members': faculty,
        'student_members': students,
    })


@admin_required
def admin_council_list(request):
    years = CouncilYear.objects.order_by('-year_label')
    selected_year_id = request.GET.get('year', '')
    members = CouncilMember.objects.select_related('council_year').order_by('council_year__year_label', 'member_type', 'order_no')
    if selected_year_id:
        members = members.filter(council_year_id=selected_year_id)
    return render(request, 'council/admin/council_list.html', {
        'title': 'Manage Council', 'years': years, 'members': members, 'selected_year': selected_year_id,
    })


@admin_required
def admin_year_add(request):
    form = CouncilYearForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        year = form.save()
        log_activity(request.user, AdminActivityLog.ActionType.CREATE, 'CouncilYear', year.pk, str(year), request=request)
        messages.success(request, f'Council year "{year.year_label}" added.')
        return redirect('council:admin_list')
    return render(request, 'council/admin/year_form.html', {'title': 'Add Council Year', 'form': form, 'action': 'Add Year'})


@admin_required
def admin_year_edit(request, pk):
    year = get_object_or_404(CouncilYear, pk=pk)
    form = CouncilYearForm(request.POST or None, instance=year)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Council year "{year.year_label}" updated.')
        return redirect('council:admin_list')
    return render(request, 'council/admin/year_form.html', {'title': f'Edit {year.year_label}', 'form': form, 'year': year, 'action': 'Save'})


@admin_required
def admin_member_add(request):
    form = CouncilMemberForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        member = form.save()
        log_activity(request.user, AdminActivityLog.ActionType.CREATE, 'CouncilMember', member.pk, member.name, request=request)
        messages.success(request, f'Member "{member.name}" added.')
        return redirect('council:admin_list')
    return render(request, 'council/admin/member_form.html', {'title': 'Add Member', 'form': form, 'action': 'Add Member'})


@admin_required
def admin_member_edit(request, pk):
    member = get_object_or_404(CouncilMember, pk=pk)
    form = CouncilMemberForm(request.POST or None, request.FILES or None, instance=member)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Member "{member.name}" updated.')
        return redirect('council:admin_list')
    return render(request, 'council/admin/member_form.html', {'title': f'Edit: {member.name}', 'form': form, 'member': member, 'action': 'Save'})


@admin_required
@require_POST
def admin_member_delete(request, pk):
    member = get_object_or_404(CouncilMember, pk=pk)
    name = member.name
    log_activity(request.user, AdminActivityLog.ActionType.DELETE, 'CouncilMember', member.pk, name, request=request)
    member.delete()
    messages.success(request, f'Member "{name}" removed.')
    return redirect('council:admin_list')
