from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("mediator", "Mediator"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)  # Added phone number field
    designation = models.CharField(max_length=100, blank=True)  # Added designation field

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True,
    )

    def __str__(self):  # String representation of the user
        return f"{self.username} ({self.role})"


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use settings.AUTH_USER_MODEL for custom user
    email = models.EmailField()

    def __str__(self):
        return self.user.username


class Case(models.Model):
    STATUS_CHOICES = (
        (0, "Draft"),
        (1, "Published"),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return self.title


class Arbitrator(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    qualifications = models.TextField()
    experience = models.PositiveIntegerField()  # Years of experience
    certification = models.TextField(blank=True)
    certification_file = models.FileField(upload_to='certifications/', blank=True)

    def __str__(self):
        return f"{self.user.username} - Arbitrator"


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
