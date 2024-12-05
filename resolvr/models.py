from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('mediator', 'Mediator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)  # Assuming you want to store a unique email

    def __str__(self):
        return self.user.username  # Return the username for representation


class Case(models.Model):
    STATUS_CHOICES = (
        (0, "Draft"),
        (1, "Published"),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)  # Add this line
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
