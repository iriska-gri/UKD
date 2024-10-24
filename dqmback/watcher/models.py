from django.db import models
from accounts.models import *
from datetime import date

# Create your models here.
class Watcher(models.Model):
    # path = models.CharField(verbose_name="Название", max_length=1000)
    user = models.ForeignKey(FNSUser, on_delete=models.CASCADE, null=True, related_name='user_looked')
    counted = models.IntegerField(default=0)
    razdel= models.CharField(verbose_name="Раздел",default="ФБ1", max_length=1000)
    date = models.DateField(default=date.today)
    class Meta:
        unique_together = (('razdel', 'user','date'),)
        # verbose_name = "Список ЕНС"
        # verbose_name_plural = "Список ЕНС"


    def __str__(self):
            return str(self.user)

