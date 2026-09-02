"""
IIC-IEM Website – Council App Models
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class CouncilYear(models.Model):
    """
    Represents a council session / academic year.
    Historical data is preserved by keeping old council years.
    """
    year_label = models.CharField(
        _('year label'),
        max_length=50,
        unique=True,
        help_text=_('e.g., "2025-2026" or "2024-25"'),
    )
    is_current = models.BooleanField(
        _('current council year'),
        default=False,
        help_text=_('Only one year should be marked as current.'),
    )
    description = models.TextField(
        _('description'),
        blank=True,
        default='',
        help_text=_('Optional notes about this council year.'),
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Council Year')
        verbose_name_plural = _('Council Years')
        ordering = ['-year_label']

    def __str__(self):
        return f"Council {self.year_label}" + (" (Current)" if self.is_current else "")

    def save(self, *args, **kwargs):
        """Ensure only one year is marked as current."""
        if self.is_current:
            CouncilYear.objects.filter(is_current=True).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class CouncilMember(models.Model):
    """
    A council member (faculty or student) for a specific council year.
    """
    class MemberType(models.TextChoices):
        FACULTY = 'faculty', _('Faculty')
        STUDENT = 'student', _('Student')

    council_year = models.ForeignKey(
        CouncilYear,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name=_('council year'),
    )
    name = models.CharField(
        _('full name'),
        max_length=300,
    )
    role = models.CharField(
        _('role / position'),
        max_length=200,
        help_text=_('e.g., President, Vice President, Faculty Advisor, Secretary'),
    )
    designation = models.CharField(
        _('designation / department'),
        max_length=300,
        blank=True,
        default='',
        help_text=_('For faculty: their academic designation. For students: branch and year.'),
    )
    member_type = models.CharField(
        _('member type'),
        max_length=20,
        choices=MemberType.choices,
        default=MemberType.STUDENT,
        db_index=True,
    )
    photo = models.ImageField(
        _('profile photo'),
        upload_to='council/photos/',
        null=True,
        blank=True,
        help_text=_('Square photo recommended. Min 300x300px.'),
    )
    email = models.EmailField(
        _('email address'),
        blank=True,
        default='',
    )
    linkedin_url = models.URLField(
        _('LinkedIn profile'),
        blank=True,
        default='',
    )
    order_no = models.PositiveSmallIntegerField(
        _('display order'),
        default=0,
        help_text=_('Lower number = displayed first. Used to sort members on the page.'),
    )
    is_active = models.BooleanField(
        _('active in this council'),
        default=True,
    )

    class Meta:
        verbose_name = _('Council Member')
        verbose_name_plural = _('Council Members')
        ordering = ['council_year', 'member_type', 'order_no', 'name']

    def __str__(self):
        return f"{self.name} – {self.role} ({self.council_year.year_label})"
