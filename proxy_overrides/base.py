from django.dispatch import receiver

from django.db.models import signals
from django.db.models.fields.related import ReverseManyToOneDescriptor


def override_model_field(model, name, field):

    original_field = model._meta.get_field(name)

    if not isinstance(field, original_field.__class__):
        raise TypeError('Model {!r} field {!r} is not compatible with {!r}'.format(
            model, name, field.__class__.__name__
        ))

    if field.remote_field:

        related_name = field.remote_field.related_name
        if not related_name:
            related_name = original_field.remote_field.get_accessor_name()
        related_model = getattr(field.remote_field.model, related_name).rel.model

        if related_model._meta.proxy:
            raise TypeError('There is already a proxy model {!r} related to {!r} using {!r}'.format(
                related_model.__name__,
                field.remote_field.model.__name__,
                related_name
            ))

    model.add_to_class(name, field)
    model._meta.local_fields.remove(field)

    if field.remote_field:
        field.remote_field.model.add_to_class(
            related_name,
            ReverseManyToOneDescriptor(field.remote_field)
        )


class ProxyField(object):
    def __init__(self, field):
        self.field = field

    def contribute_to_class(self, model, name):
        @receiver(signals.class_prepared, sender=model, weak=False)
        def late_bind(sender, *args, **kwargs):
            override_model_field(model, name, self.field)
