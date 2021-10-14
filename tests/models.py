from django.db import models
from proxy_overrides.related import ProxyForeignKey
from proxy_overrides.base import ProxyField


class Foo(models.Model):
    bar = models.ForeignKey('tests.Bar', on_delete='null')


class Bar(models.Model):
    a = models.IntegerField(default=1)


class UnrelatedFoo(models.Model):
    bar = models.ForeignKey('tests.Bar', related_name='+', on_delete='null')


class BarProxy(Bar):
    class Meta:
        proxy = True


class BarChild(Bar):
    b = models.IntegerField(default=2)


class FooProxy(Foo):
    bar = ProxyForeignKey(BarProxy, on_delete='null')

    class Meta:
        proxy = True


class FooChildProxy(Foo):
    bar = ProxyForeignKey(BarChild, on_delete='null')

    class Meta:
        proxy = True


class Baz(models.Model):
    integer = models.IntegerField(default=2)


class BazProxy(Baz):
    integer = ProxyField(models.IntegerField(default=3))

    class Meta:
        proxy = True


class UnrelatedBarProxy(Bar):
    class Meta:
        proxy = True


class UnrelatedFooProxy(UnrelatedFoo):
    bar = ProxyForeignKey(UnrelatedBarProxy, on_delete='null')

    class Meta:
        proxy = True
