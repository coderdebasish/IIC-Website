"""IIC-IEM – Gallery Admin"""
from django.contrib import admin
from .models import Album, GalleryImage

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 0

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'order_no', 'image_count', 'created_at']
    inlines = [GalleryImageInline]
