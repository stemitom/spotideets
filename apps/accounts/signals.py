# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from .models import PrivacySettings


# @receiver(post_save, sender=User)
# def create_privacy_settings(sender, instance, created, **kwargs):
#     if created:
#         PrivacySettings.objects.create(user=instance)
