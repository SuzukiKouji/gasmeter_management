from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    address3 = models.CharField(max_length=255, blank=True)
    tel = models.CharField(max_length=20)
    meter_location = models.CharField(max_length=100)
    usage_code = models.CharField(max_length=20)
    excess_category = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
