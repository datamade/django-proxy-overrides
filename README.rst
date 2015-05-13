Allow overriding fields on Proxy models.

Mostly, you won't want to do this. However, I did have a situation where it would
be useful, mainly for reducing the numbers of queries I was having to run.

You can read about it at: http://schinckel.net/2015/05/13/django-proxy-model-relations/


Usage is pretty simple:

    class ProxyModel(ParentModel):
        related = ProxyForeignKey(OtherProxyModel)

You may only override fields that exist, although in the future, it may be possible to create a relation with a different name (enabling you to keep the standard relation to the non-proxy model).

You may also only override with a compatible field, and can only point to another proxy model (and only one proxy model may point to any other given proxy model).


It is also possible to override non-related models, but I'm not that interested in that use case at the moment.