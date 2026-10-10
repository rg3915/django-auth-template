import uuid

from django.db import models


class TimeStampedModel(models.Model):
    """Preenche created e modified sozinho."""

    created = models.DateTimeField('criado em', auto_now_add=True)
    modified = models.DateTimeField('modificado em', auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Chave primária UUID em vez de 1, 2, 3..."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class ActiveQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def inactive(self):
        return self.filter(active=False)


class ActiveModel(models.Model):
    """Desativa o registro sem apagar: Model.objects.active() e .inactive()."""

    active = models.BooleanField('ativo', default=True)

    objects = ActiveQuerySet.as_manager()

    class Meta:
        abstract = True
