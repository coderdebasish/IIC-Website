"""
IIC-IEM Website – Gallery App Models
General photo gallery albums and images.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Album(models.Model):
    """
    A photo album for the general gallery section.
    """
    title = models.CharField(_('album title'), max_length=300)
    description = models.TextField(
        _('description'),
        blank=True,
        default='',
    )
    cover_image = models.ImageField(
        _('cover image'),
        upload_to='gallery/covers/',
        null=True,
        blank=True,
        help_text=_('Used as the album thumbnail on the gallery listing page.'),
    )
    is_published = models.BooleanField(_('published'), default=True)
    order_no = models.PositiveSmallIntegerField(_('display order'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')
        ordering = ['order_no', '-created_at']

    def __str__(self):
        return self.title

    @property
    def image_count(self):
        return self.images.count()


class GalleryImage(models.Model):
    """
    A single image within a gallery album.
    """
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('album'),
    )
    image = models.ImageField(
        _('image'),
        upload_to='gallery/images/',
        help_text=_('JPG or WebP recommended. Max 5MB.'),
    )
    caption = models.CharField(
        _('caption'),
        max_length=400,
        blank=True,
        default='',
    )
    order = models.PositiveSmallIntegerField(_('display order'), default=0)
    uploaded_at = models.DateTimeField(_('uploaded at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Gallery Image')
        verbose_name_plural = _('Gallery Images')
        ordering = ['album', 'order', 'uploaded_at']

    def __str__(self):
        return f"Image in '{self.album.title}' [{self.order}]"
