from django.dispatch import receiver
from django.db.models.signals import post_save

from questioning.qa.models import Question


@receiver(post_save, sender=Question)
def question_save(sender, instance=None, created=False, **kwargs):
    """保存问题时"""
    instance.home_items.update_or_create(
        user=instance.user
    )


