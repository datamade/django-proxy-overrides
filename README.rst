|Tests|

.. |Tests| image:: https://github.com/datamade/django-proxy-overrides/actions/workflows/python-publish.yml/badge.svg
   :target: https://github.com/datamade/django-proxy-overrides/actions/workflows/python-publish.yml

Allow overriding foreign key fields on Proxy models.

Mostly, you won't want to do this. However, I did have a situation where it would
be useful, mainly for reducing the numbers of queries I was having to run.

You can read about it at: http://schinckel.net/2015/05/13/django-proxy-model-relations/


Usage is pretty simple:

.. code-block :: python

    from proxy_overrides.related import ProxyForeignKey

    class ProxyModel(ParentModel):
        related = ProxyForeignKey(OtherProxyModel)

You may only override fields that exist, although in the future, it may be possible to create a relation with a different name (enabling you to keep the standard relation to the non-proxy model).
