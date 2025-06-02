from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.TextChoices):
    ADMIN = "admin", "Admin"
    STUDENT = "student", "Student"

class Status(models.TextChoices):
    FREE = "free", "Free"
    PREMIUM = "premium", "Premium"


class Account(AbstractUser):
    role = models.CharField(max_length=10, choices=Role, default=Role.STUDENT)
    status = models.CharField(max_length=10, choices=Status, default=Status.FREE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
