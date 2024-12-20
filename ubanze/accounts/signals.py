from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ServiceProviderProfile, CustomerProfile, CustomUser
import logging
logger = logging.getLogger(__name__)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    logger.info(f"Signal fired for user {instance.pk}, created={created}")
    if created:
        if instance.is_service_provider:
            logger.info(f"Creating ServiceProviderProfile for user {instance.pk}")
            ServiceProviderProfile.objects.create(user=instance)
        else:
            logger.info(f"Creating CustomerProfile for user {instance.pk}")
            CustomerProfile.objects.create(user=instance)