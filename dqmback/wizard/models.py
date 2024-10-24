from email.policy import default
from enum import unique
from django.db import models
from .models import *
from statistic.models import Passport
from accounts.models import FNSUser

class Images(models.Model):
    name =  models.CharField(verbose_name="Название изображения", max_length=50, blank=True)
    path = models.ImageField(upload_to='images/%Y/%m/%d/')
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Рисунок"
        verbose_name_plural = "Рисунки"
class Way(models.Model):
    waystep = models.CharField(verbose_name="Действие",unique=True, max_length=500)  
    
    # public = models.BooleanField(verbose_name="Вывод в чекбокс", default=True)

    def __str__(self):
        return self.waystep

    class Meta:
        verbose_name = "Действие"
        verbose_name_plural = "Действия"


class Step(models.Model):
    passport = models.ForeignKey(Passport, on_delete=models.CASCADE, verbose_name="Паспорт", null=True)
    name = models.CharField(verbose_name="Название шага", max_length=500)
    textdescription = models.TextField(verbose_name="Описание шага", blank=True)
    mode = models.TextField(verbose_name="Режим", null = True)
    images = models.ManyToManyField(Images, verbose_name="Картинки шага", related_name="imagesstep", blank=True) 
    actions = models.ManyToManyField(Way,through="StepWay",through_fields=('stepnow', 'action'))
    numberstep =  models.IntegerField(verbose_name="Номер шага", blank=True, null=True)
    def __str__(self):
        # d = 45        
        # return self.name[0:d]+'...' if len(self.name)>d else str(self.name)
        return str(self.pk)

    class Meta:
        verbose_name = 'Шаг'
        verbose_name_plural = 'Шаги'
        unique_together = (('passport', 'name','numberstep'),)

class StepWay(models.Model):
    stepnow = models.ForeignKey(Step, on_delete=models.CASCADE, verbose_name="Шаг сейчас")
    action = models.ForeignKey(Way, on_delete=models.CASCADE, verbose_name="Действие", null=True)
    nextstep = models.IntegerField(verbose_name="Номер шага", blank=True, null=True)
    # models.ForeignKey(Step, on_delete=models.CASCADE, verbose_name="Шаг потом", related_name='stepnext')
    class Meta:
        unique_together = (('stepnow', 'nextstep'),)





























    

# class PassportStep(models.Model):
#     passport = models.IntegerField(verbose_name="Номер шага", blank=True, null=True)
   
#     step =models.IntegerField(verbose_name="Номер шага", blank=True, null=True)
#     button = models.IntegerField(verbose_name="Номер шага", blank=True, null=True)
   
#     nextstep = models.IntegerField(verbose_name="Номер шага", blank=True, null=True)
#     numberstep =  models.IntegerField(verbose_name="Номер шага", blank=True, null=True)


#     def __str__(self):
#         return f'{self.passport}'

#     class Meta:
#         # unique_together = [['id_pasport']]
#         verbose_name = 'Формирование карточки'
#         verbose_name_plural = 'Формирование карточек'

# class Exemplar(models.Model):
#     name = models.CharField(verbose_name="Имя экземпляра", max_length=500)  
#     history = models.CharField(verbose_name="История шагов", max_length=1000, default = '0')
#     id_pasport = models.ForeignKey(Passport, on_delete=models.CASCADE, verbose_name="Паспорт", null=True)
#     id_author = models.ForeignKey(FNSUser, on_delete=models.CASCADE, verbose_name="Автор", null=True)

#     def __str__(self):
#         return f'{self.name}'

#     class Meta:
#         verbose_name = 'Экземпляр карточки'
#         verbose_name_plural = 'Экземпляры карточек'