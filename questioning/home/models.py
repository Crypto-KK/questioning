import uuid

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import (
    GenericRelation,
    GenericForeignKey
)
from django.utils.encoding import python_2_unicode_compatible

from questioning.utils.models import CreatedUpdatedMixin

@python_2_unicode_compatible
class Item(CreatedUpdatedMixin, models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey()

    def __str__(self):
        return self.pk

    class Meta:
        verbose_name = '首页推荐'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'content_type', 'object_id')
        index_together = ('content_type', 'object_id')
