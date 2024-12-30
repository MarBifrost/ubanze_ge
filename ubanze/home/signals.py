from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import ServiceProviderProfile
from .models import Services


@receiver(post_save, sender=ServiceProviderProfile)
def update_services_on_profile_change(sender, instance, created, **kwargs):
    if created:
        print(f"New ServiceProviderProfile created for {instance.user}")
    else:
        related_services = Services.objects.filter(user=instance.user)
        for service in related_services:
            service.area = instance.area
            service.save()
