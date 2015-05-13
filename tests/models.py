from django.db import models
from proxy_overrides.related import ProxyForeignKey
from proxy_overrides.base import ProxyField


class Foo(models.Model):
    bar = models.ForeignKey('tests.Bar')


class Bar(models.Model):
    pass


class BarProxy(Bar):
    class Meta:
        proxy = True


class FooProxy(Foo):
    bar = ProxyForeignKey(BarProxy)

    class Meta:
        proxy = True


class BarProxy2(Bar):
    class Meta:
        proxy = True


# class FooStringProxy(Foo):
#     bar = ProxyForeignKey('tests.BarProxy2')
#
#     class Meta:
#         proxy = True


class Baz(models.Model):
    integer = models.IntegerField(default=2)


class BazProxy(Baz):
    integer = ProxyField(models.IntegerField(default=3))

    class Meta:
        proxy = True
