import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import PermissionsMixin


# Create your models here.

#model for the City
class City(models.Model):
    city_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.city_name


#Model for the Area
class Area(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='area')
    area_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.area_name}, {self.city}"


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        if password is None:
            raise ValueError("The password field must be set")
        if username is None:
            raise ValueError("The Username field must be set")

        user = self.create_user(username, email, password, **extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.save()

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_service_provider = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone']

    def __str__(self):
        return self.username

    groups = models.ManyToManyField('auth.Group', related_name='customer_set', blank=True,
                                    help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                    verbose_name="groups")
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customer_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class ServiceProviderProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='service_provider_profile')
    service_title = models.CharField(max_length=255, null=True, blank=True)
    service_description = models.CharField(max_length=255, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='providers_in_city')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='providers_in_area')
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.service_title}"


class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    provider = models.ForeignKey(ServiceProviderProfile, on_delete=models.CASCADE, related_name='customer_profile')

    def __str__(self):
        return f"{self.user}-> {self.provider}"
