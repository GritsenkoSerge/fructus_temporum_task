from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    """Миксин полями даты и времени создания/изменения."""

    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    'Дата и время создания.'

    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)
    """Дата и время изменения."""

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    pk = models.UUIDField(
        _('id'),
        name='id',
        default=uuid4,
        primary_key=True,
        editable=False,
    )
    """Идентификатор."""

    class Meta:
        abstract = True
