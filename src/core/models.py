from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    pass


class Todo(models.Model):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    title = models.CharField(
        max_length=200
    )
    description = models.TextField(
        blank=True, default=""
    )
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES,
        default=MEDIUM,
    )
    complete_before = models.DateTimeField(
        null=True,
        blank=True,
        default=None
    )
    to_be_notified = models.BooleanField(
        default=False
    )
    is_notified = models.BooleanField(
        default=False
    )
    is_completed = models.BooleanField(
        default=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f"{self.description}_{self.created_at}_{self.user}".lower()
