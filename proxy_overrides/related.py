from django.db.models import ForeignKey
from .base import ProxyField


class ProxyForeignKey(ProxyField):
    def __init__(self, *args, **kwargs):
        super(ProxyForeignKey, self).__init__(ForeignKey(*args, **kwargs))
