from django.db import models
from accounts.models import User
from customers.models import Customer
from django.utils import timezone

class VisitRecord(models.Model):
    STATUS_CHOICES = (
        ('done', '完了'),
        ('absent', '不在'),
        ('retry', '再訪問'),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='visit_records'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='visit_records'
    )

    visit_date = models.DateTimeField('訪問日時')
    status = models.CharField('訪問時ステータス', max_length=20, choices=STATUS_CHOICES)
    memo = models.TextField('メモ', blank=True)

    created_at = models.DateTimeField('作成日時', default=timezone.now)

    def __str__(self):
        return f'{self.customer.name} - {self.visit_date}'

class Photo(models.Model):
    visit_record = models.ForeignKey(
        VisitRecord,
        on_delete=models.CASCADE,
        related_name='photos'
    )

    file_path = models.ImageField('画像パス', upload_to='visit_photos/')
    created_at = models.DateTimeField('作成日時', default=timezone.now)

    def __str__(self):
        return f'Photo {self.id}'