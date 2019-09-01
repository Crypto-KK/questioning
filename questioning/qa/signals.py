from django.dispatch import receiver
from django.db.models.signals import post_save

from questioning.qa.models import Question


@receiver(post_save, sender=Question)
def question_save(sender, instance=None, created=False, **kwargs):
    instance.home_items.create(
        user=instance.user
    )
