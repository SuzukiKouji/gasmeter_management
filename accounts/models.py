from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', '管理者'),
        ('staff', '巡回員'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
