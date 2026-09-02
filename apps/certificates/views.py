"""
IIC-IEM Website – Certificates App Views
Public verification + Admin management + Bulk import
"""
import uuid
import io
import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from django_htmx.http import trigger_client_event

from .models import Certificate, CertificateImportLog
from .forms import CertificateForm, CertificateImportForm, CertificateRevokeForm
from apps.users.decorators import admin_required
from apps.users.utils import log_activity
from apps.users.models import AdminActivityLog


# ─── Public: Certificate Verification ─────────────────────────────────────────

def certificate_verify_page(request):
    """Public: Certificate verification landing page with QR scanner."""
    return render(request, 'certificates/verify.html', {
        'title': 'Certificate Verification – IIC IEM',
        'meta_description': 'Verify your IIC-IEM certificate using the QR code or certificate ID.',
    })


def certificate_verify_api(request):
    """
    HTMX endpoint: verify a certificate by ID.
    Returns partial HTML for the result area.
    GET parameter: certificate_id
    """
    certificate_id = request.GET.get('certificate_id', '').strip().upper()

    if not certificate_id:
        return render(request, 'certificates/partials/verify_result.html', {
            'error': 'Please enter a Certificate ID.',
        })

    try:
        cert = Certificate.objects.select_related('event').get(
            certificate_id__iexact=certificate_id
        )
        return render(request, 'certificates/partials/verify_result.html', {
            'certificate': cert,
            'result': cert.get_public_display(),
        })
    except Certificate.DoesNotExist:
        return render(request, 'certificates/partials/verify_result.html', {
            'not_found': True,
            'searched_id': certificate_id,
        })


# ─── Admin: Certificate Management ────────────────────────────────────────────

@admin_required
def admin_certificate_list(request):
    """Admin: list all certificates with filtering."""
    from apps.events.models import Event

    event_id = request.GET.get('event', '')
    status_filter = request.GET.get('status', '')
    search = request.GET.get('q', '').strip()

    certs = Certificate.objects.select_related('event').order_by('-created_at')

    if event_id:
        certs = certs.filter(event_id=event_id)
    if status_filter:
        certs = certs.filter(status=status_filter)
    if search:
        from django.db.models import Q
        certs = certs.filter(
            Q(certificate_id__icontains=search) |
            Q(recipient_name__icontains=search)
        )

    events = Event.objects.order_by('title')

    return render(request, 'certificates/admin/certificate_list.html', {
        'title': 'Manage Certificates',
        'certificates': certs[:500],  # paginate in future
        'events': events,
        'status_choices': Certificate.Status.choices,
        'active_event': event_id,
        'active_status': status_filter,
        'search': search,
    })


@admin_required
def admin_certificate_add(request):
    """Admin: manually add a single certificate record."""
    form = CertificateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        cert = form.save()
        log_activity(request.user, AdminActivityLog.ActionType.CREATE, 'Certificate', cert.pk, cert.certificate_id, request=request)
        messages.success(request, f'Certificate {cert.certificate_id} added.')
        return redirect('certificates:admin_list')

    return render(request, 'certificates/admin/certificate_form.html', {
        'title': 'Add Certificate',
        'form': form,
        'action': 'Add Certificate',
    })


@admin_required
def admin_certificate_edit(request, pk):
    """Admin: edit a certificate record."""
    cert = get_object_or_404(Certificate, pk=pk)
    form = CertificateForm(request.POST or None, instance=cert)

    if request.method == 'POST' and form.is_valid():
        form.save()
        log_activity(request.user, AdminActivityLog.ActionType.UPDATE, 'Certificate', cert.pk, cert.certificate_id, request=request)
        messages.success(request, f'Certificate {cert.certificate_id} updated.')
        return redirect('certificates:admin_list')

    return render(request, 'certificates/admin/certificate_form.html', {
        'title': f'Edit: {cert.certificate_id}',
        'form': form,
        'certificate': cert,
        'action': 'Save Changes',
    })


@admin_required
def admin_certificate_revoke(request, pk):
    """Admin: revoke a certificate."""
    cert = get_object_or_404(Certificate, pk=pk)
    form = CertificateRevokeForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        cert.status = Certificate.Status.REVOKED
        cert.revocation_reason = form.cleaned_data['revocation_reason']
        cert.save()
        log_activity(request.user, AdminActivityLog.ActionType.REVOKE, 'Certificate', cert.pk, cert.certificate_id, cert.revocation_reason, request=request)
        messages.success(request, f'Certificate {cert.certificate_id} has been revoked.')
        return redirect('certificates:admin_list')

    return render(request, 'certificates/admin/certificate_revoke.html', {
        'title': f'Revoke: {cert.certificate_id}',
        'form': form,
        'certificate': cert,
    })


@admin_required
def admin_certificate_import(request):
    """Admin: bulk import certificates from CSV or Excel."""
    from apps.events.models import Event

    form = CertificateImportForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        uploaded_file = request.FILES['file']
        event = form.cleaned_data.get('event')
        file_name = uploaded_file.name

        # Read the file
        try:
            if file_name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, dtype=str)
            elif file_name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file, dtype=str)
            else:
                messages.error(request, 'Unsupported file format. Please upload CSV or Excel (.xlsx).')
                return redirect('certificates:admin_import')
        except Exception as e:
            messages.error(request, f'Could not read file: {e}')
            return redirect('certificates:admin_import')

        # Normalize column names
        df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

        # Required columns
        required_cols = {'certificate_id', 'recipient_name', 'certificate_type', 'issue_date'}
        missing = required_cols - set(df.columns)
        if missing:
            messages.error(request, f'Missing required columns: {", ".join(missing)}. Required: certificate_id, recipient_name, certificate_type, issue_date')
            return redirect('certificates:admin_import')

        # Create import batch
        batch_id = uuid.uuid4().hex[:12].upper()
        import_log = CertificateImportLog.objects.create(
            batch_id=batch_id,
            event=event,
            uploaded_by=request.user,
            file_name=file_name,
            total_rows=len(df),
            status=CertificateImportLog.ImportStatus.IN_PROGRESS,
        )

        imported = 0
        skipped = 0
        errors = 0
        error_details = []

        for idx, row in df.iterrows():
            try:
                cert_id = str(row.get('certificate_id', '')).strip().upper()
                if not cert_id or cert_id == 'NAN':
                    errors += 1
                    error_details.append(f"Row {idx+2}: Empty certificate_id")
                    continue

                if Certificate.objects.filter(certificate_id=cert_id).exists():
                    skipped += 1
                    error_details.append(f"Row {idx+2}: Duplicate ID – {cert_id}")
                    continue

                issue_date_raw = str(row.get('issue_date', '')).strip()
                try:
                    from datetime import datetime
                    issue_date = pd.to_datetime(issue_date_raw).date()
                except Exception:
                    errors += 1
                    error_details.append(f"Row {idx+2}: Invalid issue_date – {issue_date_raw}")
                    continue

                Certificate.objects.create(
                    certificate_id=cert_id,
                    recipient_name=str(row.get('recipient_name', '')).strip(),
                    event=event,
                    certificate_type=str(row.get('certificate_type', 'Participant')).strip(),
                    issue_date=issue_date,
                    status=Certificate.Status.VALID,
                    import_batch=batch_id,
                )
                imported += 1
            except Exception as e:
                errors += 1
                error_details.append(f"Row {idx+2}: {str(e)}")

        # Update import log
        import_log.imported_count = imported
        import_log.skipped_count = skipped
        import_log.error_count = errors
        import_log.error_details = '\n'.join(error_details)
        import_log.status = (
            CertificateImportLog.ImportStatus.COMPLETED if errors == 0
            else CertificateImportLog.ImportStatus.PARTIAL
        )
        import_log.save()

        log_activity(
            request.user, AdminActivityLog.ActionType.IMPORT, 'Certificate',
            batch_id, f'Batch {batch_id}',
            f'Imported: {imported}, Skipped: {skipped}, Errors: {errors}',
            request=request,
        )

        messages.success(
            request,
            f'Import complete – Batch {batch_id}: {imported} imported, {skipped} skipped (duplicates), {errors} errors.'
        )
        return redirect('certificates:admin_import_history')

    return render(request, 'certificates/admin/certificate_import.html', {
        'title': 'Bulk Import Certificates',
        'form': form,
    })


@admin_required
def admin_import_history(request):
    """Admin: view certificate import history."""
    logs = CertificateImportLog.objects.select_related('event', 'uploaded_by').order_by('-created_at')[:50]
    return render(request, 'certificates/admin/import_history.html', {
        'title': 'Import History',
        'logs': logs,
    })
