from django.dispatch import receiver
from django.db.models.signals import post_save

from questioning.articles.models import Article


@receiver(post_save, sender=Article)
def article_save(sender, instance=None, created=False, **kwargs):
    instance.home_items.update_or_create(
        user=instance.user
    )
