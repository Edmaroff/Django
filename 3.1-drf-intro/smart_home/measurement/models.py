from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)

class Measurement(models.Model):
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateTimeField(auto_now=True)
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE, related_name='measurements')
    photo = models.ImageField(null=True, upload_to="photos/%Y/%m/%d/")
