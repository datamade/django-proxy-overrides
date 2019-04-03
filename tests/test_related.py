from proxy_overrides.base import ProxyRelationAlreadyExists

from django.test import TestCase

from .models import Foo, Bar, FooProxy, BarProxy, BarChild, FooChildProxy


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
        with self.assertRaises(ProxyRelationAlreadyExists):
            from proxy_overrides.related import ProxyForeignKey

            class FooNewProxy(Foo):
                bar = ProxyForeignKey('BarProxy', on_delete='null')
