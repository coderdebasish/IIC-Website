"""
IIC-IEM Website – Certificates App Models
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Certificate(models.Model):
    """
    Certificate verification record.
    The website does NOT generate certificates — it only stores verification data.
    Certificate PDFs are distributed externally.
    """

    class Status(models.TextChoices):
        VALID = 'valid', _('Valid')
        REVOKED = 'revoked', _('Revoked')
        EXPIRED = 'expired', _('Expired')

    # ── Core Fields ───────────────────────────────────────────────────────────
    certificate_id = models.CharField(
        _('certificate ID'),
        max_length=200,
        unique=True,
        db_index=True,
        help_text=_('Unique certificate identifier. e.g., IIC-IEM-2026-IDEA-001'),
    )
    recipient_name = models.CharField(
        _('recipient name'),
        max_length=300,
        help_text=_('Full name of the certificate recipient.'),
    )
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='certificates',
        verbose_name=_('event'),
        help_text=_('The event this certificate is associated with.'),
    )
    certificate_type = models.CharField(
        _('certificate type'),
        max_length=200,
        default='Participant',
        help_text=_('e.g., Participant, Winner, Runner-Up, Volunteer, Speaker, Organizer'),
    )
    issue_date = models.DateField(
        _('issue date'),
        help_text=_('Date the certificate was issued.'),
    )

    # ── Status ────────────────────────────────────────────────────────────────
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=Status.choices,
        default=Status.VALID,
        db_index=True,
    )
    revocation_reason = models.TextField(
        _('revocation reason'),
        blank=True,
        default='',
        help_text=_('Required when revoking a certificate. Not shown publicly.'),
    )

    # ── Admin Notes ───────────────────────────────────────────────────────────
    notes = models.TextField(
        _('internal notes'),
        blank=True,
        default='',
        help_text=_('Internal admin notes. Not visible to the public.'),
    )

    # ── Import Tracking ───────────────────────────────────────────────────────
    import_batch = models.CharField(
        _('import batch ID'),
        max_length=100,
        blank=True,
        default='',
        help_text=_('Batch identifier for bulk imports. Helps track which upload this came from.'),
    )

    # ── Timestamps ────────────────────────────────────────────────────────────
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Certificate')
        verbose_name_plural = _('Certificates')
        ordering = ['-issue_date', 'certificate_id']
        indexes = [
            models.Index(fields=['certificate_id']),
            models.Index(fields=['status']),
            models.Index(fields=['event', 'status']),
            models.Index(fields=['import_batch']),
        ]

    def __str__(self):
        return f"{self.certificate_id} – {self.recipient_name}"

    @property
    def is_valid(self) -> bool:
        return self.status == self.Status.VALID

    def get_public_display(self) -> dict:
        """
        Returns only the fields safe to display publicly during verification.
        Excludes internal notes and revocation reasons.
        """
        return {
            'certificate_id': self.certificate_id,
            'recipient_name': self.recipient_name,
            'event_name': self.event.title if self.event else 'N/A',
            'certificate_type': self.certificate_type,
            'issue_date': self.issue_date,
            'status': self.get_status_display(),
            'is_valid': self.is_valid,
        }


class CertificateImportLog(models.Model):
    """
    Tracks bulk import operations for certificates.
    """
    class ImportStatus(models.TextChoices):
        IN_PROGRESS = 'in_progress', _('In Progress')
        COMPLETED = 'completed', _('Completed')
        FAILED = 'failed', _('Failed')
        PARTIAL = 'partial', _('Partially Completed')

    batch_id = models.CharField(
        _('batch ID'),
        max_length=100,
        unique=True,
    )
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('event'),
    )
    uploaded_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('uploaded by'),
    )
    file_name = models.CharField(_('original file name'), max_length=500)
    total_rows = models.PositiveIntegerField(_('total rows'), default=0)
    imported_count = models.PositiveIntegerField(_('imported'), default=0)
    skipped_count = models.PositiveIntegerField(_('skipped / duplicates'), default=0)
    error_count = models.PositiveIntegerField(_('errors'), default=0)
    status = models.CharField(
        _('import status'),
        max_length=20,
        choices=ImportStatus.choices,
        default=ImportStatus.IN_PROGRESS,
    )
    error_details = models.TextField(_('error details'), blank=True, default='')
    created_at = models.DateTimeField(_('imported at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Certificate Import Log')
        verbose_name_plural = _('Certificate Import Logs')
        ordering = ['-created_at']

    def __str__(self):
        return f"Import [{self.batch_id}] – {self.file_name} ({self.status})"
