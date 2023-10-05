from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import CustomUser

from .models import PrivacySettings


@receiver(post_save, sender=CustomUser)
def create_privacy_settings(sender, instance, created, **kwargs):
    if created:
        PrivacySettings.objects.create(user=instance)
