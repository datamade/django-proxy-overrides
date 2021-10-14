from django.db.models import IntegerField
from django.test import TestCase
from django.db import models

from proxy_overrides.base import ProxyField
from .models import (
    Foo,
    Bar,
    UnrelatedFoo,
    FooProxy,
    BarProxy,
    BarChild,
    FooChildProxy,
    UnrelatedFooProxy,
    UnrelatedBarProxy,
)


class TestRelated(TestCase):
    def test_original_relation(self):
        bar = Bar.objects.create()
        Foo.objects.create(bar=bar)

        foo = Foo.objects.get()
        self.assertEqual(Foo, foo.__class__)
        self.assertEqual(Bar, foo.bar.__class__)

    def test_fk_field_override(self):
        bar = Bar.objects.create()
        Foo.objects.create(bar=bar)

        foo = FooProxy.objects.get()

        self.assertEqual(
            FooProxy,
            foo.__class__
        )

        self.assertEqual(
            BarProxy,
            foo.bar.__class__
        )

    def test_fk_child_override_child(self):
        bar_child = BarChild.objects.create()
        Foo.objects.create(bar=bar_child)

        foo = FooChildProxy.objects.get()

        self.assertEqual(
            FooChildProxy,
            foo.__class__
        )

        self.assertEqual(
            BarChild,
            foo.bar.__class__
        )

        assert foo.bar.a == 1
        assert foo.bar.b == 2

    def test_reverse_fk_field_override(self):
        bar = Bar.objects.create()
        Foo.objects.create(bar=bar)

        bar = BarProxy.objects.get()

        self.assertEqual(
            BarProxy,
            bar.__class__
        )

        self.assertEqual(
            FooProxy,
            bar.foo_set.model
        )

    def test_reverse_fk_field_child_child(self):
        bar_child = BarChild.objects.create()
        Foo.objects.create(bar=bar_child)

        bar_child = BarChild.objects.get()

        self.assertEqual(
            BarChild,
            bar_child.__class__
        )

        self.assertEqual(
            FooChildProxy,
            bar_child.foo_set.model
        )

    def test_exception_if_same_relation(self):
        with self.assertRaises(TypeError) as e:
            from proxy_overrides.related import ProxyForeignKey

            class FooNewProxy(Foo):
                bar = ProxyForeignKey(BarProxy, on_delete=models.SET_NULL)

        self.assertEqual(
            "There is already a proxy model 'BarProxy' related to 'BarProxy' "
            "using 'foo_set'",
            str(e.exception)
        )

    def test_field_compatibility(self):
        with self.assertRaises(TypeError) as e:

            class ProxyIntegerField(ProxyField):
                def __init__(self, *args, **kwargs):
                    super(ProxyIntegerField, self).__init__(IntegerField(*args, **kwargs))

            class FooNewProxy(Foo):
                bar = ProxyIntegerField()

        self.assertEqual(
            "Model <class 'tests.test_related.TestRelated.test_field_compatibility.<locals>.FooNewProxy'> "
            "field 'bar' is not compatible with 'IntegerField'",
            str(e.exception)
        )

    def test_unrelated_proxy(self):
        bar = Bar.objects.create()
        UnrelatedFoo.objects.create(bar=bar)

        foo = UnrelatedFooProxy.objects.get()

        self.assertEqual(
            UnrelatedFooProxy,
            foo.__class__
        )

        self.assertEqual(
            UnrelatedBarProxy,
            foo.bar.__class__
        )
