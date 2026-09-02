"""
IIC-IEM Website – Users App Utility: Activity Logger
"""
from functools import wraps
from .models import AdminActivityLog


def log_activity(admin_user, action, model_name, object_id='', object_repr='', details='', request=None):
    """
    Utility function to log admin activities.
    Call this after any significant admin action.
    """
    ip_address = None
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')

    AdminActivityLog.objects.create(
        admin_user=admin_user,
        action=action,
        model_name=model_name,
        object_id=str(object_id),
        object_repr=str(object_repr)[:500],
        details=str(details)[:2000],
        ip_address=ip_address,
    )
