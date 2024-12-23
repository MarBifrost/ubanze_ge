from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ServiceProviderProfile, CustomerProfile, CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_service_provider:
            ServiceProviderProfile.objects.get_or_create(user=instance)
        else:
            CustomerProfile.objects.get_or_create(user=instance)
