from django.db import models
from django.conf import settings
from customers.models import Customer

class VisitRecord(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    visit_date = models.DateTimeField()
    status = models.CharField(max_length=20)
    inspection_due_date = models.DateField()
    value_status = models.CharField(max_length=20)
    current_model = models.CharField(max_length=50)
    current_serial_number = models.CharField(max_length=50)
    reason = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Photo(models.Model):
    visit_record = models.ForeignKey(
        VisitRecord,
        related_name='photos',
        on_delete=models.CASCADE
    )
    file_path = models.ImageField(upload_to='visit_photos/')
    created_at = models.DateTimeField(auto_now_add=True)