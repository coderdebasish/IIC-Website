"""
IIC-IEM Website – Core Models (Site Settings)
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    """
    Singleton model for global site configuration.
    Only one row should exist. Use SiteSettings.get_settings() to retrieve.
    """
    # ── Identity ──────────────────────────────────────────────────────────────
    site_name = models.CharField(
        _('site name'),
        max_length=200,
        default='IIC – IEM',
    )
    tagline = models.CharField(
        _('tagline'),
        max_length=500,
        default='Institution\'s Innovation Council | IEM Kolkata',
        blank=True,
    )
    logo = models.ImageField(
        _('logo'),
        upload_to='site/',
        null=True,
        blank=True,
        help_text=_('Recommended: PNG with transparent background, min 200px height.'),
    )
    favicon = models.ImageField(
        _('favicon'),
        upload_to='site/',
        null=True,
        blank=True,
        help_text=_('Square image, 32x32 or 64x64 px.'),
    )

    # ── Hero Section ──────────────────────────────────────────────────────────
    hero_tagline = models.CharField(
        _('hero tagline'),
        max_length=300,
        default='Fostering Innovation & Entrepreneurship',
        blank=True,
    )
    hero_description = models.TextField(
        _('hero description'),
        default='The Institution\'s Innovation Council at IEM Kolkata works to promote a culture of innovation, creativity, and entrepreneurship among students.',
        blank=True,
    )
    hero_background = models.ImageField(
        _('hero background image'),
        upload_to='site/',
        null=True,
        blank=True,
    )

    # ── Leadership / President's Message ─────────────────────────────────────
    president_name = models.CharField(
        _('president name'),
        max_length=200,
        default='Prof. Dr. Satyajit Chakrabarti',
        blank=True,
    )
    president_designation = models.CharField(
        _('president designation'),
        max_length=300,
        default='President, IIC IEM & President, IEM UEM Group',
        blank=True,
    )
    president_message = models.TextField(
        _('president message'),
        default='The IEM UEM Group has set sublime standards in addressing technical and managerial innovation. Our Institution\'s Innovation Council serves as a catalyst for student startups, research breakthroughs, and national-level entrepreneurship.',
        blank=True,
    )
    president_image = models.ImageField(
        _('president photo'),
        upload_to='site/',
        null=True,
        blank=True,
        help_text=_('Photo of President / Director.'),
    )

    # ── About ─────────────────────────────────────────────────────────────────
    about_iic = models.TextField(
        _('about IIC'),
        blank=True,
        default='',
        help_text=_('Rich text about IIC at national level.'),
    )
    about_iic_at_iem = models.TextField(
        _('about IIC at IEM'),
        blank=True,
        default='',
        help_text=_('Specific information about IIC at IEM Kolkata.'),
    )
    vision = models.TextField(
        _('vision'),
        blank=True,
        default='',
    )
    mission = models.TextField(
        _('mission'),
        blank=True,
        default='',
    )
    objectives = models.TextField(
        _('objectives'),
        blank=True,
        default='',
        help_text=_('List the key objectives. Can use newlines.'),
    )

    # ── Contact ───────────────────────────────────────────────────────────────
    contact_email = models.EmailField(
        _('contact email'),
        blank=True,
        default='',
    )
    contact_phone = models.CharField(
        _('contact phone'),
        max_length=50,
        blank=True,
        default='',
    )
    contact_address = models.TextField(
        _('contact address'),
        blank=True,
        default='',
    )

    # ── Social Media ──────────────────────────────────────────────────────────
    facebook_url = models.URLField(_('Facebook URL'), blank=True, default='')
    instagram_url = models.URLField(_('Instagram URL'), blank=True, default='')
    twitter_url = models.URLField(_('Twitter / X URL'), blank=True, default='')
    linkedin_url = models.URLField(_('LinkedIn URL'), blank=True, default='')
    youtube_url = models.URLField(_('YouTube URL'), blank=True, default='')
    website_url = models.URLField(_('Official Website URL'), blank=True, default='')

    # ── Footer ────────────────────────────────────────────────────────────────
    footer_text = models.TextField(
        _('footer text'),
        blank=True,
        default='© IIC – IEM Kolkata. All Rights Reserved.',
    )
    footer_links_json = models.TextField(
        _('footer quick links (JSON)'),
        blank=True,
        default='',
        help_text=_('JSON array of {label, url} objects for footer quick links.'),
    )

    # ── SEO ───────────────────────────────────────────────────────────────────
    meta_description = models.TextField(
        _('default meta description'),
        max_length=300,
        blank=True,
        default='Official website of the Institution\'s Innovation Council (IIC) at IEM Kolkata.',
    )
    meta_keywords = models.CharField(
        _('meta keywords'),
        max_length=500,
        blank=True,
        default='IIC, IEM, innovation, council, Kolkata, entrepreneurship',
    )
    google_analytics_id = models.CharField(
        _('Google Analytics ID'),
        max_length=50,
        blank=True,
        default='',
        help_text=_('e.g., G-XXXXXXXXXX'),
    )

    # ── Timestamps ────────────────────────────────────────────────────────────
    updated_at = models.DateTimeField(_('last updated'), auto_now=True)

    class Meta:
        verbose_name = _('Site Settings')
        verbose_name_plural = _('Site Settings')

    def __str__(self):
        return f"Site Settings ({self.site_name})"

    @classmethod
    def get_settings(cls):
        """
        Retrieve the singleton SiteSettings object.
        Creates a default instance if none exists.
        """
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def get_social_links(self) -> list:
        """Returns a list of active social links as dicts."""
        links = []
        social_map = [
            ('facebook_url', 'Facebook', 'fab fa-facebook-f'),
            ('instagram_url', 'Instagram', 'fab fa-instagram'),
            ('twitter_url', 'Twitter / X', 'fab fa-x-twitter'),
            ('linkedin_url', 'LinkedIn', 'fab fa-linkedin-in'),
            ('youtube_url', 'YouTube', 'fab fa-youtube'),
        ]
        for field, label, icon in social_map:
            url = getattr(self, field)
            if url:
                links.append({'label': label, 'url': url, 'icon': icon})
        return links
