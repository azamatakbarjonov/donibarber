from django.db import models

class Price(models.Model):
    price = models.CharField(max_length=2, blank=True, null=True, verbose_name='soch narxi')
