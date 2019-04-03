from django.db import models
from proxy_overrides.related import ProxyForeignKey
from proxy_overrides.base import ProxyField


class Foo(models.Model):
    bar = models.ForeignKey('tests.Bar', on_delete='null')


class Bar(models.Model):
    a = models.IntegerField(default=1)


class BarProxy(Bar):
    class Meta:
        proxy = True


class BarChild(Bar):
    b = models.IntegerField(default=2)


class FooProxy(Foo):
    # reference related model directly
    bar = ProxyForeignKey(BarProxy, on_delete='null')

    class Meta:
        proxy = True


class FooChildProxy(Foo):
    # related model passed as string
    bar = ProxyForeignKey('BarChild', on_delete='null')

    class Meta:
        proxy = True


class Baz(models.Model):
    integer = models.IntegerField(default=2)


class BazProxy(Baz):
    integer = ProxyField(models.IntegerField(default=3))

    class Meta:
        proxy = True
