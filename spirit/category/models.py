# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from .managers import CategoryQuerySet
from ..core.utils.models import AutoSlugField


class Category(models.Model):

    parent = models.ForeignKey('self', verbose_name=_("category parent"), null=True, blank=True)

    title = models.CharField(_("title"), max_length=75)
    slug = AutoSlugField(populate_from="title", db_index=False, blank=True)
    description = models.CharField(_("description"), max_length=255, blank=True)
    is_global = models.BooleanField(_("global"), default=True,
                                    help_text=_('Designates whether the topics will be'
                                                'displayed in the all-categories list.'))
    is_closed = models.BooleanField(_("closed"), default=False)
    is_removed = models.BooleanField(_("removed"), default=False)
    is_private = models.BooleanField(_("private"), default=False)

    # topic_count = models.PositiveIntegerField(_("topic count"), default=0)

    objects = CategoryQuerySet.as_manager()

    class Meta:
        ordering = ['title', 'pk']
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def get_absolute_url(self):
        if self.pk == settings.ST_TOPIC_PRIVATE_CATEGORY_PK:
            return reverse('spirit:topic:private:index')
        else:
            return reverse('spirit:category:detail', kwargs={'pk': str(self.id), 'slug': self.slug})

    @property
    def is_subcategory(self):
        if self.parent_id:
            return True
        else:
            return False


# def topic_posted_handler(sender, topic, **kwargs):
#    if topic.category.is_subcategory:
#        category = Category.objects.filter(pk__in=[topic.category.pk, topic.category.parent.pk])
#    else:
#        category = Category.objects.filter(pk=topic.category.pk)
#
#    category.update(topic_count=F('topic_count') + 1)


# topic_posted.connect(topic_posted_handler, dispatch_uid=__name__)
