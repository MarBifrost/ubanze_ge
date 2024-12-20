import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import PermissionsMixin


# Create your models here.


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

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        user = self.create_user(username, email, password, **extra_fields)
        user.save(using=self._db)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=12, blank=True, null=True, unique=True, validators=[RegexValidator(regex=r'^\d+$',message="Phone number must contain only numbers.", code='invalid_phone_number')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer_type = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_service_provider = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

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


class CustomerType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.type_name

class ServiceProviderProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='service_provider_profile')
    city = models.ForeignKey('home.City', on_delete=models.CASCADE, related_name='providers_in_city', null=True, blank=True)
    area = models.ForeignKey('home.Area', on_delete=models.CASCADE, related_name='providers_in_area', null=True, blank=True)
    street=models.CharField(max_length=255, blank=True, null=True)
    service_category = models.ForeignKey('home.ServiceCategory', on_delete=models.CASCADE, related_name='providers_in_category', null=True, blank=True)
    service_description = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"


class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    provider = models.ForeignKey(ServiceProviderProfile, on_delete=models.CASCADE, related_name='customer_profile')

    def __str__(self):
        return f"{self.user}-> {self.provider}"


class EmailQueue(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='email_queue')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    recipient_email=models.EmailField()
    sent=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

