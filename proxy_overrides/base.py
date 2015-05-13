from django.dispatch import receiver

from django.db.models import signals
from django.db.models.fields.related import ForeignRelatedObjectsDescriptor


def override_model_field(model, name, field):

    original_field = model._meta.get_field(name)

    if not isinstance(field, original_field.__class__):
        raise TypeError('Model {!r} field {!r} is not compatible with {!r}'.format(
            model, name, field.__class__.__name__
        ))

    if field.rel:
        # Ensure we are referencing another proxy class.
        if not field.rel.to._meta.proxy:
            raise TypeError('You must relate to another proxy class, not {!r}'.format(
                field.rel.to.__name__
            ))

        related_name = getattr(field, 'related_name', original_field.related.get_accessor_name())
        related_model = getattr(field.rel.to, related_name).related.model
        if related_model._meta.proxy:
            raise TypeError('There is already a proxy model {!r} related to {!r} using {!r}'.format(
                related_model.__name__,
                field.rel.to.__name__,
                related_name
            ))

    model.add_to_class(name, field)

    if field.rel:
        field.rel.to.add_to_class(
            related_name,
            ForeignRelatedObjectsDescriptor(field.related)
        )


class ProxyField(object):
    def __init__(self, field):
        self.field = field

    def contribute_to_class(self, model, name):
        @receiver(signals.class_prepared, sender=model, weak=False)
        def late_bind(sender, *args, **kwargs):
            override_model_field(model, name, self.field)
