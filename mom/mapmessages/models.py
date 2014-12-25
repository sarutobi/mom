# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    """ Message categories """
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


class MessageQueryset(GeoQuerySet):
    def list(self):
        """ Ask only few fields for listing"""

        return self.values(
            'id', 'title', 'message', 'messageType',
            'date_add', )

    def active(self):
        return self.filter(
            status__gt=Message.NEW, status__lt=Message.CLOSED,
            is_removed=False
        )

    def closed(self):
        return self.filter(status=Message.CLOSED)

    def type_is(self, m_type):
        return self.filter(messageType=m_type)

    def is_deleted(self):
        return self.filter(is_removed=True)


class Message(models.Model):
    """ Message data """

    class Meta():
        ordering = ['-date_add']
        get_latest_by = 'date_add'
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    # Message status
    NEW = 1
    UNVERIFIED = 2
    VERIFIED = 3
    PENDING = 4
    CLOSED = 6

    MESSAGE_STATUS = ((NEW, _('New')),
                      (UNVERIFIED, _('Unverified')),
                      (VERIFIED, _('Verified')),
                      (PENDING, _('Pending')),
                      (CLOSED, _('Closed')))

    # Main message fields
    title = models.CharField(
        max_length=200,
        verbose_name=_('title'),
        blank=True)
    message = models.TextField(verbose_name=_('Message'))
    # Link to message author.
    status = models.SmallIntegerField(
        choices=MESSAGE_STATUS,
        verbose_name=_('status'),
        default=NEW, blank=True, null=True
    )
    start_date = models.DateTimeField(
        verbose_name=_("started at"),
        blank=True, null=True)
    expired_date = models.DateTimeField(
        verbose_name=_("expired at"),
        blank=True, null=True
    )
    address = models.CharField(
        max_length=200,
        verbose_name=_("address"),
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
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        editable=False,
        db_column='user_id',
    )
    # Moderator's fields
    # Message can be inactive, i.e. not 'closed' and no more information can be
    # added.
    is_active = models.BooleanField(
        default=False, verbose_name=_('active')
    )
    # Is it urgent message?
    is_important = models.BooleanField(
        default=False, verbose_name=_('important')
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
        return self.title or "Untitled"

    def get_absolute_url(self):
        return reverse_lazy("message-details", args=[str(self.pk)])


class MessageNotes(models.Model):
    """ Moderator notes for message """

    message = models.ForeignKey(Message)
    user = models.ForeignKey(User, editable=False, verbose_name=_("Author"))
    note = models.TextField(verbose_name=_("Note"))
    date_add = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Created at"))
    last_edit = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_("Last edit"))

    def __unicode__(self):
        return _("Note from %(user)s to message %(msgid)d")\
            % {'user': self.user, 'msgid': self.message_id, }
