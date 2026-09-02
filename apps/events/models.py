"""
IIC-IEM Website – Events App Models
Complete event system: Event, EventContent, EventStage, EventReport, EventGalleryImage
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


class Event(models.Model):
    """
    Core event model. Each event has its own page, lifecycle, content, gallery, and report.
    """
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        UPCOMING = 'upcoming', _('Upcoming')
        ONGOING = 'ongoing', _('Ongoing')
        COMPLETED = 'completed', _('Completed')
        ARCHIVED = 'archived', _('Archived')

    # ── Core Information ──────────────────────────────────────────────────────
    title = models.CharField(
        _('event title'),
        max_length=300,
    )
    slug = models.SlugField(
        _('URL slug'),
        max_length=350,
        unique=True,
        help_text=_('Auto-generated from title. Used in the event URL. Must be unique.'),
    )
    short_description = models.TextField(
        _('short description'),
        max_length=600,
        help_text=_('Brief description shown on event cards and listing pages. Max 600 chars.'),
    )
    poster = models.ImageField(
        _('event poster / cover image'),
        upload_to='events/posters/',
        null=True,
        blank=True,
        help_text=_('Recommended: 16:9 ratio, min 1200px wide, JPG or PNG.'),
    )

    # ── Dates ─────────────────────────────────────────────────────────────────
    start_date = models.DateTimeField(
        _('start date & time'),
    )
    end_date = models.DateTimeField(
        _('end date & time'),
        null=True,
        blank=True,
        help_text=_('Optional. For single-day events, leave blank.'),
    )

    # ── Status & Visibility ───────────────────────────────────────────────────
    status = models.CharField(
        _('event status'),
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    is_featured = models.BooleanField(
        _('featured on homepage'),
        default=False,
        help_text=_('Show this event in the Featured section on the homepage.'),
    )

    # ── Registration ──────────────────────────────────────────────────────────
    registration_link = models.URLField(
        _('registration link'),
        blank=True,
        default='',
        help_text=_('External registration URL (e.g., Google Form). Leave blank to hide the Register button.'),
    )
    registration_deadline = models.DateTimeField(
        _('registration deadline'),
        null=True,
        blank=True,
        help_text=_('Optional. Informational only – does not auto-close the link.'),
    )

    # ── Category / Tags ───────────────────────────────────────────────────────
    category = models.CharField(
        _('category'),
        max_length=100,
        blank=True,
        default='',
        help_text=_('e.g., Workshop, Hackathon, Seminar, Competition, Webinar'),
    )
    tags = models.CharField(
        _('tags'),
        max_length=500,
        blank=True,
        default='',
        help_text=_('Comma-separated tags for filtering. e.g., innovation, AI, startup'),
    )

    # ── Venue ─────────────────────────────────────────────────────────────────
    venue = models.CharField(
        _('venue'),
        max_length=500,
        blank=True,
        default='',
        help_text=_('Physical venue or "Online" or "Hybrid"'),
    )
    venue_link = models.URLField(
        _('venue map link'),
        blank=True,
        default='',
        help_text=_('Optional Google Maps or other map link.'),
    )

    # ── Meta ──────────────────────────────────────────────────────────────────
    created_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_events',
        verbose_name=_('created by'),
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['status', '-start_date']),
            models.Index(fields=['slug']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not set."""
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('events:detail', kwargs={'slug': self.slug})

    @property
    def is_upcoming(self) -> bool:
        return self.status == self.Status.UPCOMING

    @property
    def is_past(self) -> bool:
        return self.status in (self.Status.COMPLETED, self.Status.ARCHIVED)

    @property
    def has_registration(self) -> bool:
        return bool(self.registration_link)

    @property
    def date_display(self) -> str:
        """Human-readable date range."""
        if self.end_date and self.end_date.date() != self.start_date.date():
            return f"{self.start_date.strftime('%d %b %Y')} – {self.end_date.strftime('%d %b %Y')}"
        return self.start_date.strftime('%d %B %Y')

    def get_tag_list(self) -> list:
        """Returns tags as a list."""
        if self.tags:
            return [t.strip() for t in self.tags.split(',') if t.strip()]
        return []


class EventContent(models.Model):
    """
    Rich text content area for an event's detail page.
    One-to-one with Event. Created automatically with the event.
    """
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name='content',
        verbose_name=_('event'),
    )
    content = CKEditor5Field(
        _('content'),
        config_name='default',
        blank=True,
        default='',
        help_text=_('Rich content for the event detail page. Use the editor to add text, images, tables, links, etc.'),
    )
    updated_at = models.DateTimeField(_('last updated'), auto_now=True)

    class Meta:
        verbose_name = _('Event Content')
        verbose_name_plural = _('Event Contents')

    def __str__(self):
        return f"Content for: {self.event.title}"


class EventStage(models.Model):
    """
    Custom lifecycle stage for an event.
    Each event has its own set of stages, ordered by stage_order.
    """
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='stages',
        verbose_name=_('event'),
    )
    name = models.CharField(
        _('stage name'),
        max_length=200,
        help_text=_('e.g., "Registration Open", "Event Day", "Certificates Available"'),
    )
    description = models.CharField(
        _('stage description'),
        max_length=500,
        blank=True,
        default='',
        help_text=_('Optional brief description of this stage.'),
    )
    stage_order = models.PositiveSmallIntegerField(
        _('order'),
        default=0,
        help_text=_('Lower number = earlier stage. Stages are displayed left-to-right.'),
    )
    start_date = models.DateField(
        _('start date'),
        null=True,
        blank=True,
        help_text=_('Informational only. Does not auto-trigger status changes.'),
    )
    end_date = models.DateField(
        _('end date'),
        null=True,
        blank=True,
    )
    is_current = models.BooleanField(
        _('current stage'),
        default=False,
        help_text=_('Mark this as the currently active stage. Only one stage should be current per event.'),
    )
    is_completed = models.BooleanField(
        _('completed'),
        default=False,
        help_text=_('Mark this stage as completed (shown with a checkmark).'),
    )

    class Meta:
        verbose_name = _('Event Stage')
        verbose_name_plural = _('Event Stages')
        ordering = ['event', 'stage_order']
        unique_together = [['event', 'stage_order']]

    def __str__(self):
        return f"{self.event.title} → {self.name}"

    def save(self, *args, **kwargs):
        """Ensure only one stage is marked as 'current' per event."""
        if self.is_current:
            EventStage.objects.filter(event=self.event, is_current=True).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class EventReport(models.Model):
    """
    Event report. Can contain rich text and/or file/link attachments.
    One-to-one with Event.
    """
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name='report',
        verbose_name=_('event'),
    )
    content = CKEditor5Field(
        _('report content'),
        config_name='default',
        blank=True,
        default='',
        help_text=_('Write the event report here. Supports rich text, images, tables.'),
    )
    pdf_file = models.FileField(
        _('report PDF'),
        upload_to='events/reports/',
        null=True,
        blank=True,
        help_text=_('Optional: Upload a PDF report.'),
    )
    external_link = models.URLField(
        _('external report link'),
        blank=True,
        default='',
        help_text=_('Optional: Link to report on Google Drive or elsewhere.'),
    )
    is_published = models.BooleanField(
        _('published'),
        default=False,
        help_text=_('Uncheck to hide the report from the public while editing.'),
    )
    updated_at = models.DateTimeField(_('last updated'), auto_now=True)

    class Meta:
        verbose_name = _('Event Report')
        verbose_name_plural = _('Event Reports')

    def __str__(self):
        return f"Report: {self.event.title}"


class EventGalleryImage(models.Model):
    """
    Individual image in an event's gallery.
    """
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        verbose_name=_('event'),
    )
    image = models.ImageField(
        _('image'),
        upload_to='events/gallery/',
        help_text=_('Recommended: JPG or WebP, max 5MB.'),
    )
    caption = models.CharField(
        _('caption'),
        max_length=300,
        blank=True,
        default='',
    )
    order = models.PositiveSmallIntegerField(
        _('display order'),
        default=0,
    )
    uploaded_at = models.DateTimeField(_('uploaded at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Event Gallery Image')
        verbose_name_plural = _('Event Gallery Images')
        ordering = ['event', 'order', 'uploaded_at']

    def __str__(self):
        return f"Image [{self.order}] for {self.event.title}"
