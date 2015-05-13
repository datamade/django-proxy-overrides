from django.db import models
from django.test import TestCase

from proxy_overrides.base import ProxyField

from .models import Baz, BazProxy


class TestFieldOverride(TestCase):
    def test_override_compatible(self):
        baz = Baz.objects.create()
        self.assertEquals(2, baz.integer)

        baz_proxy = BazProxy.objects.create()
        self.assertEquals(3, baz_proxy.integer)

    def test_override_incompatible(self):

        with self.assertRaises(TypeError):
            class BadBazProxy(Baz):
                integer = ProxyField(models.CharField(max_length=128, default='4'))

                class Meta:
                    proxy = True

    def test_override_non_existent_field(self):

        with self.assertRaises(models.FieldDoesNotExist):
            class BadBazProxy(Baz):
                other = ProxyField(models.IntegerField(default=3))

                class Meta:
                    proxy = True
