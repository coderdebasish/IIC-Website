"""
IIC-IEM Website – Announcements App Models
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Announcement(models.Model):
    """
    Site-wide announcement. Can be pinned to homepage.
    """

    class Priority(models.TextChoices):
        NORMAL = 'normal', _('Normal')
        IMPORTANT = 'important', _('Important')
        URGENT = 'urgent', _('Urgent')

    title = models.CharField(_('title'), max_length=400)
    content = models.TextField(
        _('content'),
        help_text=_('The announcement text. Supports basic formatting.'),
    )
    link = models.URLField(
        _('call-to-action link'),
        blank=True,
        default='',
        help_text=_('Optional: URL for a "Read More" or action button.'),
    )
    link_text = models.CharField(
        _('link button text'),
        max_length=100,
        blank=True,
        default='Read More',
        help_text=_('Text for the link button, if a link is provided.'),
    )
    priority = models.CharField(
        _('priority'),
        max_length=20,
        choices=Priority.choices,
        default=Priority.NORMAL,
    )
    is_active = models.BooleanField(
        _('active / published'),
        default=True,
        help_text=_('Uncheck to hide this announcement without deleting it.'),
    )
    show_on_home = models.BooleanField(
        _('show on homepage'),
        default=True,
        help_text=_('Show this announcement in the homepage announcements section.'),
    )
    expires_at = models.DateTimeField(
        _('expires at'),
        null=True,
        blank=True,
        help_text=_('Optional: Auto-hide this announcement after this date/time.'),
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Announcement')
        verbose_name_plural = _('Announcements')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_visible(self) -> bool:
        """Returns True if the announcement is active and not expired."""
        if not self.is_active:
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        return True

    @classmethod
    def get_active(cls):
        """Returns currently visible announcements."""
        now = timezone.now()
        return cls.objects.filter(
            is_active=True
        ).filter(
            models.Q(expires_at__isnull=True) | models.Q(expires_at__gt=now)
        )
