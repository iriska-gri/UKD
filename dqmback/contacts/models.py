from email.mime import image
from django.db import models
from django.forms import ImageField
from accounts.models import FNSUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import FileExtensionValidator
from asgiref.sync import sync_to_async,async_to_sync
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from django.db.models import Count
from statistic.models import Passport

class Contacts(models.Model):
    phone = models.CharField(verbose_name="Телефон поддержки", max_length=25, blank=True,)
    email = models.CharField(verbose_name="Электронная почта", max_length=250, blank=True,)
    topblock = RichTextUploadingField(verbose_name="Блок 1")
    # bottomblock = RichTextUploadingField(verbose_name="Блок 2")
    imagepath =  models.ImageField(upload_to = "contactsimg/%Y/%m/%d", height_field=None, width_field=None, max_length=100, null=True,verbose_name="Картинка")
    class Meta:
        verbose_name = "ТП"
        verbose_name_plural = "ТП"
    def __str__(self):
        return "Техподдержка"

class SupportPassportMetodolog(models.Model):
    methodolog = models.OneToOneField(FNSUser, on_delete=models.PROTECT, verbose_name="Методолог",null=True,blank=True)
    connectedPassport = models.ManyToManyField(Passport, verbose_name="Паспорта")

    class Meta:
            verbose_name = "Методолог-паспорта"
            verbose_name_plural = "Методологи-паспорта"
    def __str__(self):
        return str(self.methodolog)



class Questions(models.Model):
    asker = models.ForeignKey(FNSUser, on_delete=models.PROTECT, verbose_name="Кто задал вопрос",null=True,blank=True)
    question = models.TextField(verbose_name="Вопрос")
    questiondate = models.DateTimeField(verbose_name="Время подачи вопроса", auto_now_add=True)
    answer = models.TextField(verbose_name="Ответ")
    answerer = models.ForeignKey(FNSUser, on_delete=models.PROTECT, verbose_name="Кто ответил",related_name="qanswerer",null=True,blank=True)
    answerdate = models.DateTimeField(verbose_name="Время ответа", null=True, blank=True)
    status = models.BooleanField(verbose_name="Ответ отправлен", default=False)
    readed =  models.BooleanField(verbose_name="Прочитано", default=False)
    last_reader = models.ForeignKey(FNSUser, on_delete=models.PROTECT, verbose_name="Последний",related_name="qreader",null=True,blank=True)
    readedtime = models.DateTimeField(verbose_name="Время просмотра", null=True, blank=True)
    def __str__(self):
        return str(self.question)[0:50]
    class Meta:
        verbose_name = "Вопрос в техподдержку"
        verbose_name_plural = "Вопросы в техподдержку"
        


    

# class Adress(models.Model):
#     name= models.CharField(verbose_name="Заголовок", max_length=125, blank=True,)
#     text = RichTextUploadingField(verbose_name="Текст")

#     def __str__(self):
#         return str(self.name)
#     class Meta:
#         unique_together = (('name', 'text'),)
#         verbose_name = "Контакт"
#         verbose_name_plural = "Контакты"

class QuestionFiles(models.Model):    
    attachmentfile = models.FileField(verbose_name="Файл",upload_to="questionfiles/%Y/%m/%d")
    quest = models.ForeignKey(Questions, on_delete=models.CASCADE, null=True,related_name='question_files')
    
    class Meta:        
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
        default_related_name = 'question_files'

    def __str__(self):
            return str('Файл')
        
@receiver(post_save, sender=Questions)
@receiver(post_delete, sender=Questions)
def only_after_q_changed(sender,  **kwargs):
    
    layer = get_channel_layer()   
      
    waiting_questions= list(Questions.objects.all().order_by("status").values("status").annotate(count= Count("status")))             
    async_to_sync(layer.group_send)(
    'informer',
    {
        'type': 'chat_message',
        'message': {'waiting_questions': waiting_questions
    }}
    
    )
    