from django.db import models
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField('お客様名', max_length=100)
    address1 = models.CharField('住所', max_length=255)
    address2 = models.CharField('丁目番地号', max_length=255, blank=True)
    address3 = models.CharField('アパート名', max_length=255, blank=True)
    latitude = models.DecimalField('緯度', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('経度', max_digits=9, decimal_places=6, null=True, blank=True)
    tel = models.CharField('電話番号', max_length=20, blank=True)
    inspection_dur_date = models.DateField('検定年月', null=True, blank=True)
    valv_status = models.CharField('開閉栓', max_length=20)
    current_model = models.CharField('現取付型号', max_length=100)
    current_serial_number = models.CharField('現社番', max_length=100)
    meter_location = models.CharField('メーター設置位置', max_length=255)
    usage_code = models.CharField('用途コード', max_length=50)
    excess_category = models.CharField('超過分類', max_length=50)
    reason = models.TextField('事由', blank=True)
    created_at = models.DateTimeField('作成日時', default=timezone.now)

    def __str__(self):
        return self.name
