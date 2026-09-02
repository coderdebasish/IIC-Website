"""IIC-IEM – Certificates Admin"""
from django.contrib import admin
from .models import Certificate, CertificateImportLog

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['certificate_id', 'recipient_name', 'event', 'certificate_type', 'issue_date', 'status']
    list_filter = ['status', 'certificate_type']
    search_fields = ['certificate_id', 'recipient_name']
    ordering = ['-issue_date']

@admin.register(CertificateImportLog)
class CertificateImportLogAdmin(admin.ModelAdmin):
    list_display = ['batch_id', 'file_name', 'event', 'imported_count', 'skipped_count', 'error_count', 'status', 'created_at']
    readonly_fields = ['batch_id', 'file_name', 'total_rows', 'imported_count', 'skipped_count', 'error_count', 'error_details', 'created_at']
    ordering = ['-created_at']
