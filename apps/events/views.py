"""
IIC-IEM Website – Events App Views (Public + Admin)
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction

from .models import Event, EventContent, EventStage, EventReport, EventGalleryImage
from .forms import (
    EventForm, EventContentForm, EventStageForm,
    EventReportForm, EventGalleryImageForm
)
from apps.users.decorators import admin_required
from apps.users.utils import log_activity
from apps.users.models import AdminActivityLog


# ─── Public Views ──────────────────────────────────────────────────────────────

def event_list(request):
    """Public: events listing page — upcoming and past."""
    filter_type = request.GET.get('filter', 'upcoming')
    category = request.GET.get('category', '')

    upcoming = Event.objects.filter(
        status__in=['upcoming', 'ongoing']
    ).exclude(status='draft').order_by('start_date')

    past = Event.objects.filter(
        status__in=['completed', 'archived']
    ).order_by('-start_date')

    if category:
        upcoming = upcoming.filter(category__icontains=category)
        past = past.filter(category__icontains=category)

    # Collect all unique categories for the filter bar
    all_categories = Event.objects.exclude(
        category=''
    ).values_list('category', flat=True).distinct()

    context = {
        'title': 'Events – IIC IEM',
        'meta_description': 'Explore all upcoming and past events organized by the Institution\'s Innovation Council at IEM Kolkata.',
        'upcoming_events': upcoming,
        'past_events': past,
        'all_categories': sorted(set(all_categories)),
        'active_filter': filter_type,
        'active_category': category,
    }
    return render(request, 'events/event_list.html', context)


def event_detail(request, slug):
    """Public: event detail page."""
    event = get_object_or_404(
        Event.objects.prefetch_related('stages', 'gallery_images'),
        slug=slug,
        status__in=['upcoming', 'ongoing', 'completed', 'archived']
    )

    # Safely get or create related objects
    content, _ = EventContent.objects.get_or_create(event=event)
    report = getattr(event, 'report', None)
    stages = event.stages.order_by('stage_order')
    gallery = event.gallery_images.order_by('order')

    context = {
        'title': f"{event.title} – IIC IEM",
        'meta_description': event.short_description,
        'event': event,
        'content': content,
        'report': report,
        'stages': stages,
        'gallery': gallery,
    }
    return render(request, 'events/event_detail.html', context)


# ─── Admin Views ───────────────────────────────────────────────────────────────

@admin_required
def admin_event_list(request):
    """Admin: list all events."""
    status_filter = request.GET.get('status', '')
    events = Event.objects.all().order_by('-created_at')
    if status_filter:
        events = events.filter(status=status_filter)

    context = {
        'title': 'Manage Events',
        'events': events,
        'status_choices': Event.Status.choices,
        'active_status': status_filter,
    }
    return render(request, 'events/admin/event_list.html', context)


@admin_required
def admin_event_create(request):
    """Admin: create new event."""
    form = EventForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            # Auto-create content and report objects
            EventContent.objects.get_or_create(event=event)
            EventReport.objects.get_or_create(event=event)

        log_activity(request.user, AdminActivityLog.ActionType.CREATE, 'Event', event.pk, event.title, request=request)
        messages.success(request, f'Event "{event.title}" created. Now add content and lifecycle stages.')
        return redirect('events:admin_content', pk=event.pk)

    return render(request, 'events/admin/event_form.html', {
        'title': 'Create New Event',
        'form': form,
        'action': 'Create Event',
    })


@admin_required
def admin_event_detail(request, pk):
    """Admin: event management hub — overview of all sections."""
    event = get_object_or_404(Event, pk=pk)
    content = EventContent.objects.filter(event=event).first()
    report = getattr(event, 'report', None)
    stages = event.stages.order_by('stage_order')
    gallery = event.gallery_images.order_by('order')

    return render(request, 'events/admin/event_detail.html', {
        'title': f'Manage: {event.title}',
        'event': event,
        'content': content,
        'report': report,
        'stages': stages,
        'gallery': gallery,
    })


@admin_required
def admin_event_edit(request, pk):
    """Admin: edit event basic info."""
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, request.FILES or None, instance=event)

    if request.method == 'POST' and form.is_valid():
        form.save()
        log_activity(request.user, AdminActivityLog.ActionType.UPDATE, 'Event', event.pk, event.title, 'Basic info updated', request=request)
        messages.success(request, 'Event updated successfully.')
        return redirect('events:admin_detail', pk=event.pk)

    return render(request, 'events/admin/event_form.html', {
        'title': f'Edit: {event.title}',
        'form': form,
        'event': event,
        'action': 'Save Changes',
    })


@admin_required
def admin_event_content(request, pk):
    """Admin: edit event rich content."""
    event = get_object_or_404(Event, pk=pk)
    content, _ = EventContent.objects.get_or_create(event=event)
    form = EventContentForm(request.POST or None, instance=content)

    if request.method == 'POST' and form.is_valid():
        form.save()
        log_activity(request.user, AdminActivityLog.ActionType.UPDATE, 'EventContent', event.pk, event.title, 'Content updated', request=request)
        messages.success(request, 'Event content saved.')
        return redirect('events:admin_content', pk=event.pk)

    return render(request, 'events/admin/event_content.html', {
        'title': f'Content: {event.title}',
        'form': form,
        'event': event,
    })


@admin_required
def admin_event_stages(request, pk):
    """Admin: manage event lifecycle stages."""
    event = get_object_or_404(Event, pk=pk)
    stages = event.stages.order_by('stage_order')
    return render(request, 'events/admin/event_stages.html', {
        'title': f'Lifecycle: {event.title}',
        'event': event,
        'stages': stages,
    })


@admin_required
def admin_stage_add(request, pk):
    """Admin: add a lifecycle stage."""
    event = get_object_or_404(Event, pk=pk)
    form = EventStageForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        stage = form.save(commit=False)
        stage.event = event
        stage.save()
        messages.success(request, f'Stage "{stage.name}" added.')
        return redirect('events:admin_stages', pk=event.pk)

    return render(request, 'events/admin/stage_form.html', {
        'title': f'Add Stage – {event.title}',
        'form': form,
        'event': event,
        'action': 'Add Stage',
    })


@admin_required
def admin_stage_edit(request, pk, stage_pk):
    """Admin: edit a lifecycle stage."""
    event = get_object_or_404(Event, pk=pk)
    stage = get_object_or_404(EventStage, pk=stage_pk, event=event)
    form = EventStageForm(request.POST or None, instance=stage)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Stage "{stage.name}" updated.')
        return redirect('events:admin_stages', pk=event.pk)

    return render(request, 'events/admin/stage_form.html', {
        'title': f'Edit Stage – {stage.name}',
        'form': form,
        'event': event,
        'stage': stage,
        'action': 'Save Stage',
    })


@admin_required
@require_POST
def admin_stage_delete(request, pk, stage_pk):
    """Admin: delete a lifecycle stage."""
    event = get_object_or_404(Event, pk=pk)
    stage = get_object_or_404(EventStage, pk=stage_pk, event=event)
    name = stage.name
    stage.delete()
    messages.success(request, f'Stage "{name}" deleted.')
    return redirect('events:admin_stages', pk=event.pk)


@admin_required
@require_POST
def admin_stage_set_current(request, pk, stage_pk):
    """Admin: mark a stage as the current stage (HTMX-friendly)."""
    event = get_object_or_404(Event, pk=pk)
    stage = get_object_or_404(EventStage, pk=stage_pk, event=event)
    stage.is_current = True
    stage.save()  # model.save() clears other is_current flags
    messages.success(request, f'"{stage.name}" is now the current stage.')
    return redirect('events:admin_stages', pk=event.pk)


@admin_required
def admin_event_report(request, pk):
    """Admin: manage event report."""
    event = get_object_or_404(Event, pk=pk)
    report, _ = EventReport.objects.get_or_create(event=event)
    form = EventReportForm(request.POST or None, request.FILES or None, instance=report)

    if request.method == 'POST' and form.is_valid():
        form.save()
        log_activity(request.user, AdminActivityLog.ActionType.UPDATE, 'EventReport', event.pk, event.title, 'Report updated', request=request)
        messages.success(request, 'Event report saved.')
        return redirect('events:admin_report', pk=event.pk)

    return render(request, 'events/admin/event_report.html', {
        'title': f'Report: {event.title}',
        'form': form,
        'event': event,
        'report': report,
    })


@admin_required
def admin_event_gallery(request, pk):
    """Admin: event gallery management."""
    event = get_object_or_404(Event, pk=pk)
    gallery = event.gallery_images.order_by('order')
    return render(request, 'events/admin/event_gallery.html', {
        'title': f'Gallery: {event.title}',
        'event': event,
        'gallery': gallery,
    })


@admin_required
def admin_gallery_upload(request, pk):
    """Admin: upload images to event gallery."""
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        files = request.FILES.getlist('images')
        count = 0
        for f in files:
            if f.content_type in ['image/jpeg', 'image/png', 'image/webp', 'image/gif']:
                EventGalleryImage.objects.create(event=event, image=f)
                count += 1
        if count:
            log_activity(request.user, AdminActivityLog.ActionType.IMPORT, 'EventGalleryImage', event.pk, event.title, f'{count} images uploaded', request=request)
            messages.success(request, f'{count} image(s) uploaded successfully.')
        else:
            messages.warning(request, 'No valid images were uploaded. Accepted formats: JPG, PNG, WebP, GIF.')
        return redirect('events:admin_gallery', pk=event.pk)

    return redirect('events:admin_gallery', pk=event.pk)


@admin_required
@require_POST
def admin_gallery_image_delete(request, pk, img_pk):
    """Admin: delete a gallery image."""
    event = get_object_or_404(Event, pk=pk)
    image = get_object_or_404(EventGalleryImage, pk=img_pk, event=event)
    image.image.delete(save=False)
    image.delete()
    messages.success(request, 'Image deleted.')
    return redirect('events:admin_gallery', pk=event.pk)


@admin_required
@require_POST
def admin_event_delete(request, pk):
    """Admin: delete an event (only drafts or archived)."""
    event = get_object_or_404(Event, pk=pk)
    if event.status not in ['draft', 'archived']:
        messages.error(request, 'Only Draft or Archived events can be deleted. Archive the event first.')
        return redirect('events:admin_detail', pk=pk)

    title = event.title
    log_activity(request.user, AdminActivityLog.ActionType.DELETE, 'Event', event.pk, title, request=request)
    event.delete()
    messages.success(request, f'Event "{title}" has been deleted.')
    return redirect('events:admin_list')
