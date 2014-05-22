#-*- coding: utf-8 -*-

from django.test import TestCase
from django.db import models

from spirit.utils.models import AutoSlugField


class AutoSlugModel(models.Model):

    slug = AutoSlugField(max_length=50)

    class Meta:
        app_label = 'spirit'


class AutoSlugDefaultModel(models.Model):

    slug = AutoSlugField(max_length=50, default="foo")

    class Meta:
        app_label = 'spirit'


class AutoSlugPopulateFromModel(models.Model):

    title = models.CharField(max_length=255, blank=True)
    slug = AutoSlugField(populate_from='title', max_length=50)

    class Meta:
        app_label = 'spirit'


class UtilsModelsTests(TestCase):

    def test_auto_slug_field(self):
        """
        Should behave like a regular SlugField if populate_from is not provided
        """
        foo_model = AutoSlugModel(slug="foo")
        foo_model.save()
        self.assertEqual(foo_model.slug, "foo")

        foo_model = AutoSlugModel()
        foo_model.save()
        self.assertEqual(foo_model.slug, "")

    def test_auto_slug_field_default(self):
        """
        AutoSlugField default
        """
        foo_model = AutoSlugDefaultModel()
        foo_model.save()
        self.assertEqual(foo_model.slug, "foo")

        foo_model = AutoSlugDefaultModel(slug="bar")
        foo_model.save()
        self.assertEqual(foo_model.slug, "bar")

    def test_auto_slug_field_populate_from(self):
        """
        AutoSlugField populate_from
        """
        title = "a" * 255
        foo_model = AutoSlugPopulateFromModel(title=title)
        foo_model.save()
        self.assertEqual(foo_model.slug, title[:50])

        # update
        foo_model.title = "foo"
        foo_model.save()
        self.assertEqual(foo_model.slug, title[:50])

        # populate_from field is blank
        foo_model = AutoSlugPopulateFromModel()
        self.assertEqual(foo_model.slug, "")