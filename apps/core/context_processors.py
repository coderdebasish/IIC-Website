"""
IIC-IEM Website – Core Context Processor
Makes site settings and nav data available in every template.
"""
from django.core.cache import cache
from .models import SiteSettings


def site_settings(request):
    """
    Injects SiteSettings into every template context.
    Cached for 5 minutes to avoid a DB hit on every request.
    """
    settings_obj = cache.get('site_settings_singleton')
    if not settings_obj:
        settings_obj = SiteSettings.get_settings()
        cache.set('site_settings_singleton', settings_obj, 300)  # 5 min cache

    return {
        'site_settings': settings_obj,
        'social_links': settings_obj.get_social_links(),
    }
