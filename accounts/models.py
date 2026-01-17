from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', '管理者'),
        ('staff', '巡回員'),
    )
    name = models.CharField('担当者名', max_length=100)
    email = models.EmailField('メールアドレス', unique=True)
    role = models.CharField('権限', max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField('作成日時', default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    def __str__(self):
        return self.name
