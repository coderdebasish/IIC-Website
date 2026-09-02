"""
IIC-IEM Website – Custom User Model
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Custom user model for IIC-IEM admin system.
    Extends AbstractUser with role-based access control.
    """

    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        SUPER_ADMIN = 'super_admin', _('Super Admin')

    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required. A valid email address.')
    )

    role = models.CharField(
        _('role'),
        max_length=20,
        choices=Role.choices,
        default=Role.ADMIN,
        help_text=_('Admin: manage content. Super Admin: manage admins + settings.')
    )

    profile_photo = models.ImageField(
        _('profile photo'),
        upload_to='admin_profiles/',
        null=True,
        blank=True,
    )

    bio = models.TextField(
        _('bio / notes'),
        blank=True,
        default='',
        help_text=_('Optional internal notes about this admin.')
    )

    last_login_ip = models.GenericIPAddressField(
        _('last login IP'),
        null=True,
        blank=True,
    )

    # Make email the login identifier
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('Admin User')
        verbose_name_plural = _('Admin Users')
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_super_admin(self) -> bool:
        """Returns True if this user has Super Admin privileges."""
        return self.role == self.Role.SUPER_ADMIN or self.is_superuser

    @property
    def is_admin_role(self) -> bool:
        """Returns True if this user has at least Admin privileges."""
        return self.role in (self.Role.ADMIN, self.Role.SUPER_ADMIN) or self.is_staff

    def get_display_name(self) -> str:
        """Returns the best available display name."""
        return self.get_full_name() or self.username


class AdminActivityLog(models.Model):
    """
    Lightweight activity log for admin actions.
    Tracks important changes made through the admin panel.
    """

    class ActionType(models.TextChoices):
        CREATE = 'create', _('Created')
        UPDATE = 'update', _('Updated')
        DELETE = 'delete', _('Deleted')
        IMPORT = 'import', _('Imported')
        REVOKE = 'revoke', _('Revoked')
        LOGIN = 'login', _('Logged In')
        LOGOUT = 'logout', _('Logged Out')
        PUBLISH = 'publish', _('Published')
        UNPUBLISH = 'unpublish', _('Unpublished')

    admin_user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='activity_logs',
        verbose_name=_('Admin User'),
    )

    action = models.CharField(
        _('action'),
        max_length=20,
        choices=ActionType.choices,
    )

    model_name = models.CharField(
        _('model'),
        max_length=100,
        help_text=_('The Django model that was affected.'),
    )

    object_id = models.CharField(
        _('object ID'),
        max_length=200,
        blank=True,
        default='',
        help_text=_('Primary key or identifier of the affected object.'),
    )

    object_repr = models.CharField(
        _('object representation'),
        max_length=500,
        blank=True,
        default='',
        help_text=_('String representation of the object at time of action.'),
    )

    details = models.TextField(
        _('details'),
        blank=True,
        default='',
        help_text=_('Additional context about the action.'),
    )

    ip_address = models.GenericIPAddressField(
        _('IP address'),
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Activity Log')
        verbose_name_plural = _('Activity Logs')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.admin_user} {self.get_action_display()} {self.model_name} [{self.object_id}]"
