"""
IIC-IEM Website – Achievements, Gallery, Announcements Models
"""
# achievements/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class Achievement(models.Model):
    """IIC achievement, award, or milestone."""

    class Category(models.TextChoices):
        AWARD = 'award', _('Award')
        RECOGNITION = 'recognition', _('Recognition')
        MILESTONE = 'milestone', _('Milestone')
        RANKING = 'ranking', _('Ranking')
        OTHER = 'other', _('Other')

    title = models.CharField(_('title'), max_length=400)
    description = models.TextField(_('description'))
    image = models.ImageField(
        _('image'),
        upload_to='achievements/',
        null=True,
        blank=True,
    )
    date = models.DateField(
        _('date'),
        null=True,
        blank=True,
        help_text=_('Date of the achievement or award.'),
    )
    category = models.CharField(
        _('category'),
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
        db_index=True,
    )
    is_featured = models.BooleanField(
        _('featured on homepage'),
        default=False,
    )
    external_link = models.URLField(
        _('reference link'),
        blank=True,
        default='',
        help_text=_('Optional link for more information about this achievement.'),
    )
    order_no = models.PositiveSmallIntegerField(_('display order'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Achievement')
        verbose_name_plural = _('Achievements')
        ordering = ['-date', '-created_at']

    def __str__(self):
        return self.title
