from django.db import models
from django.contrib.auth.models import AbstractUser


class AccountRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    STUDENT = "student", "Student"

class AccountStatus(models.TextChoices):
    FREE = "free", "Free"
    PREMIUM = "premium", "Premium"


class Account(AbstractUser):
    role = models.CharField(max_length=10, choices=AccountRole, default=AccountRole.STUDENT)
    status = models.CharField(max_length=10, choices=AccountStatus, default=AccountStatus.FREE)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = [phone_number]

    def __str__(self):
        return self.phone_number
