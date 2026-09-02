"""IIC-IEM – Events Admin"""
from django.contrib import admin
from .models import Event, EventContent, EventStage, EventReport, EventGalleryImage

class EventStageInline(admin.TabularInline):
    model = EventStage
    extra = 1
    ordering = ['stage_order']

class EventGalleryInline(admin.TabularInline):
    model = EventGalleryImage
    extra = 0

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'start_date', 'is_featured', 'created_at']
    list_filter = ['status', 'is_featured', 'category']
    search_fields = ['title', 'slug', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [EventStageInline, EventGalleryInline]
    ordering = ['-start_date']
