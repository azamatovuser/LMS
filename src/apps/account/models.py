from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    STUDENT = "student", "Student"

class SubscriptionType(models.TextChoices):
    FREE = "free", "Free"
    PREMIUM = "premium", "Premium"

class Subscription(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='subscription')
    type = models.CharField(max_length=10, choices=SubscriptionType, default=SubscriptionType.FREE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.type}"

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = None
    date_joined = None
    last_login = None
    
    role = models.CharField(max_length=10, choices=UserRole, default=UserRole.STUDENT)
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number
