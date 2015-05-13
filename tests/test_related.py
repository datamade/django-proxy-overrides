from django.test import TestCase

from .models import Foo, Bar, FooProxy, BarProxy


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

    def test_exception_if_not_proxy_target(self):
        with self.assertRaises(TypeError):
            from proxy_overrides.related import ProxyForeignKey

            class FooNewProxy(Foo):
                bar = ProxyForeignKey(Bar)

    def test_exception_if_same_relation(self):
        with self.assertRaises(TypeError):
            from proxy_overrides.related import ProxyForeignKey

            class FooNewProxy(Foo):
                bar = ProxyForeignKey(BarProxy)
