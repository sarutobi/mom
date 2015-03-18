# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    """ Event categories """
    class Meta:
        ordering = ['order']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    name = models.CharField(
        max_length=200, db_column='name',
        verbose_name=_('name'))
    description = models.TextField(
        blank=True, db_column='description',
        verbose_name=_('description'))
    slug = models.SlugField(
        max_length=255, db_column='slug',
        verbose_name=_('slug'), blank=True)
    order = models.SmallIntegerField(db_column='order')

    def __unicode__(self):
        return self.name


class Event(models.Model):
    """ Event data """

    class Meta():
        ordering = ['-date_add']
        get_latest_by = 'date_add'
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    # Main message fields
    title = models.CharField(
        max_length=200,
        verbose_name=_('Title'),
        blank=True)
    message = models.TextField(verbose_name=_('Message'))

    started_at = models.DateTimeField(
        verbose_name=_("Started at"),
        blank=True, null=True)
    finished_at = models.DateTimeField(
        verbose_name=_("Expired at"),
        blank=True, null=True
    )
    address = models.CharField(
        max_length=200,
        verbose_name=_("Address"),
        blank=True
    )
    location = models.MultiPointField(
        verbose_name=_('On map'),
        blank=True, null=True)

    category = models.ManyToManyField(
        Category,
        symmetrical=False,
        verbose_name=_("message categories"),
        null=True, blank=True
    )
    source = models.CharField(
        max_length=255,
        verbose_name=_('source'),
        blank=True)
    # Moderator's fields
    # Message can be inactive
    is_active = models.BooleanField(
        default=False, verbose_name=_('active')
    )

    #Internal fields
    date_add = models.DateTimeField(
        auto_now_add=True,
        db_column='date_add',
        editable=False
    )
    last_edit = models.DateTimeField(
        auto_now=True,
        db_column='date_modify',
        editable=False
    )

    objects = models.GeoManager()

    def __unicode__(self):
        return self.title or _("Untitled")

    def get_absolute_url(self):
        return reverse_lazy("message-details", args=[str(self.pk)])
