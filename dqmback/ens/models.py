from django.db import models
from accounts.models import FNSUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import FileExtensionValidator
from asgiref.sync import sync_to_async,async_to_sync
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from statistic.models import Region,Priority,ResponsibleMonitoring,Criticality
def logged_user():       
        return 1

# class Region(models.Model):

#     tax_code = models.CharField(verbose_name="Код", max_length=5)
#     name = models.CharField(verbose_name="Регион", max_length=150)

#     def __str__(self):
#         return f'{self.tax_code}-{self.name}'

        
#     class Meta:
#         verbose_name = "Регион"
#         verbose_name_plural = "Регион"
#         ordering = ('tax_code',)


# class ResponsibleMonitoring(models.Model):
#     name = models.CharField(verbose_name="Имя ответственного", max_length=100, blank=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Ответственный"
#         verbose_name_plural = "Ответственные"


class SubSystem(models.Model):
    name = models.CharField(verbose_name="Имя подсистемы", max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подсистема"
        verbose_name_plural = "Подситемы"


# class Criticality(models.Model):
#     name = models.CharField(verbose_name="Название", max_length=100, blank=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Критичность"
#         verbose_name_plural = "Критичности"


# class Priority(models.Model):
#     name = models.CharField(verbose_name="Название", max_length=100, blank=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Приоритет"
#         verbose_name_plural = "Приоритеты"


class DescriptionData(models.Model):

    responsible = models.ForeignKey(ResponsibleMonitoring, on_delete=models.SET_NULL, related_name="responsens", verbose_name="Ответственный", blank=True, null=True)
    sub_system = models.ManyToManyField(SubSystem, verbose_name="Подсистема")
    criticality = models.ForeignKey(Criticality, on_delete=models.SET_NULL, verbose_name="Критичность", related_name="criticalyens", blank=True, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, verbose_name="Приоритет",related_name="priority_ens", blank=True, null=True)
    
    reason_occurrence = models.TextField(verbose_name="Причина возникновения", blank=True)
    detection_method = models.TextField(verbose_name="Способ выявления", blank=True)
    probability_of_occurrence = models.BooleanField(verbose_name="Вероятность возникновения", blank=True, null=True)

    algorithm_creation_period = models.DateField(verbose_name="Срок создания алгоритма", blank=True, null=True)
    selection_aproval_period = models.DateField(verbose_name="Срок согласования отбора", blank=True, null=True)
    date_of_formation_of_the_initial_list = models.DateField(verbose_name="Дата формирования первоначального перечня", blank=True, null=True)
    count_into_the_initial_list = models.CharField(verbose_name="Количество в первоначальном перечне", max_length=100, blank=True, null=True)

    description_algorithm = models.TextField(verbose_name="Описание алгоритма", blank=True)
    external_sources = models.TextField(verbose_name="Необходимость получения дополнительных сведений из внешних источников", blank=True)

    reason_occurrence_new = models.CharField(verbose_name="Причина возникновения новых", max_length=300, blank=True)
    measures_to_eliminate_causes = models.CharField(verbose_name="Меры по исключению причин возникновения", max_length=500, blank=True)
    application_numbers = models.CharField(verbose_name="Номера заявок в СУТ", max_length=60, blank=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = "Описание ненормализованных данных"
        verbose_name_plural = "Описания ненормализованных данных"





class Passport(models.Model):
    BOOL_CHOICES = ((True, 'Мониторинг'), (False, 'Нормализация'))
    code = models.CharField(verbose_name="Код", max_length=10)
    name = models.CharField(verbose_name="Название", max_length=250, default="")
    description = models.TextField(verbose_name="Описание", blank=True)
    code_name_process = models.TextField(verbose_name="Код и наименование технологического процесса", blank=True)
    date_of_including_of_the_initial_list = models.DateField(verbose_name="Дата включения паспорта в перечень", blank=True, null=True)
    date_of_deactivate = models.DateField(verbose_name="Дата признания неактуальным", blank=True, null=True)
    mode = models.BooleanField(verbose_name="Режим паспорта", blank=True, null=True, choices=BOOL_CHOICES)
    description_data = models.OneToOneField(DescriptionData, on_delete=models.SET_NULL, verbose_name="Описание ненормализованных данных", blank=True, null=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Паспорт ЕНС"
        verbose_name_plural = "Паспорта ЕНС"

# class PassportOff(models.Model):
#     passport = models.ForeignKey(Passport, on_delete=models.PROTECT, verbose_name="Паспорт")
#     datefrom = models.DateField(verbose_name="Исключить с (включительно)")
#     dateto = models.DateField(verbose_name="Исключить по (включительно)", blank=True, null=True)
#     type_error = models.SmallIntegerField(verbose_name='Тип ошибки',  help_text="1 - Старая , 2 - Новая, 3 - ВПНД")
#     def __str__(self):
#         return self.passport.code
#     class Meta:
#         verbose_name = "Отключить Паспорт"
#         verbose_name_plural = "Отключить Паспорта"

class ReasonForNotNormalizing(models.Model):

    # number = models.IntegerField(verbose_name="Номер", blank=True, null=True)
    name = models.CharField(verbose_name="Название", max_length=200, default="")
    # perioddead=models.IntegerField(verbose_name="Крайний срок (дней)", blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Причина ненормализации"
        verbose_name_plural = "Причины ненормализации"


class ListDataFBone(models.Model):
    
    date_unloading = models.DateField(verbose_name="Дата выгрузки", db_index=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, verbose_name="Регион",related_name='region_ens')
    passport = models.ForeignKey(Passport, on_delete=models.PROTECT, verbose_name="Паспорт", blank=True)
    fid = models.CharField(verbose_name="ФИД", max_length=25, blank=True)
    inn = models.CharField(verbose_name="ИНН", max_length=25, blank=True,)
    ogrn = models.CharField(verbose_name="ОГРН/ОГРНИП", max_length=25, blank=True)
    id_error = models.CharField(verbose_name="ID ошибки", max_length=100, blank=True, db_index=True)
    type_error = models.SmallIntegerField(verbose_name='Тип ошибки', blank=True, default=None, null=True, help_text="1 - Старая , 2 - Новая, 3 - ВПНД")
    nocode=  models.CharField(verbose_name="Код НО", max_length=15, blank=True)
    rocode= models.CharField(verbose_name="Код РО", max_length=15, blank=True)

    def __str__(self):
        return self.id_error

    class Meta:
        unique_together = (('id_error', 'date_unloading','passport'),)
        verbose_name = "Список ЕНС"
        verbose_name_plural = "Список ЕНС"





# class Justify(models.Model):
#     BOOL_CHOICES = ((True, 'Согласовано'), (False, 'Не согласовано'),(None,'На согласовании'))
#     listdate = models.OneToOneField(ListDataFBone,  on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пояснение")
#     reason = models.ForeignKey(ReasonForNotNormalizing, on_delete=models.CASCADE, null=True, blank=True)
#     description = models.TextField(verbose_name="Комментарий УФНС", blank=True)
#     date_of_justification = models.DateField(verbose_name="Дата внесения обоснования", auto_now_add=True)
#     agreement_date = models.DateField(verbose_name="Дата согласованиея", blank=True, null=True)
#     methodologist_note=models.TextField(verbose_name="Комментарий методолога", blank=True)
#     methodologist = models.ForeignKey(FNSUser,on_delete=models.CASCADE, verbose_name="Методолог",null=True)
#     fix_status = models.BooleanField(verbose_name="Статус согласования", null=True,blank=True,choices=BOOL_CHOICES)
    

#     def __str__(self):
#         if self.listdate:
#             return self.listdate.id_error
#         else:
#             return str(self.reason)

#     class Meta:
#         verbose_name = "Исключение"
#         verbose_name_plural = "Исключения"

# class JustifyFiles(models.Model):
#     HELPCH = ((True, 'Методолог'), (False, 'УФНС'))
#     justif = models.ForeignKey(Justify, on_delete=models.CASCADE, null=True, blank=True, related_name='justifiles')
#     file = models.FileField(verbose_name="Файл",upload_to="justifiles/%Y/%m/%d", null=True, blank=True)
#     author = models.BooleanField(verbose_name="Кто прислал", blank=True, null=True, choices=HELPCH)

# class Dynamics(models.Model):
#     date_unloading = models.DateField(verbose_name="Дата отчета", db_index=True)
#     file = models.FileField(verbose_name="Файл",upload_to="dynamicfiles/%Y/%m/%d")
#     name = models.CharField(verbose_name="Название", max_length=200, default="")

#     class Meta:
#         verbose_name = "Динамика"
#         verbose_name_plural = "Динамика"


Statname = [("FB1", "ФБ1"),
            ("FB2", "ФБ2"),
            ("FB3", "ФБ3"),       
            ]



# class Documentation(models.Model):
#     doc = models.CharField(verbose_name="Распоряжение", max_length=1000)
#     statistictype = models.CharField(max_length=3, choices=Statname, default="FB1", unique=True, verbose_name="Раздел")
#     file = models.FileField(verbose_name="Файл",upload_to="docfiles/%Y/%m/%d", validators=[FileExtensionValidator(['pdf'])],null=True, blank=True)
    
#     def __str__(self):
#             return str(self.doc)[0:100]
    
#     class Meta:
#         unique_together = ('doc', 'statistictype')
#         verbose_name = "Распоряжение"
#         verbose_name_plural = "Распоряжения"
#         default_related_name = 'documents'
        
# class DocumentationFiles(models.Model):
    
#     name = models.CharField(verbose_name="Название", max_length=1000)
#     attachmentfile = models.FileField(verbose_name="Файл",upload_to="docfiles/%Y/%m/%d")
#     dock = models.ForeignKey(Documentation, on_delete=models.CASCADE, null=True,related_name='document_files')
    
#     class Meta:
        
#         verbose_name = "Приложение"
#         verbose_name_plural = "Приложения"
#         default_related_name = 'document_files'

#     def __str__(self):
#             return str(self.name)[0:100]

        
# class AdditionallettersFiles(models.Model):
#     BOOL_CHOICES = ((True, 'Дополнительное письмо'), (False, 'Перечень'),)
#     name = models.CharField(verbose_name="Название", max_length=1000)
#     attachmentfile = models.FileField(verbose_name="Файл",upload_to="docfiles/%Y/%m/%d")
#     dock = models.ForeignKey(Documentation, on_delete=models.CASCADE, null=True,related_name='addition_files')
#     typin = models.BooleanField(verbose_name="Тип", default=True, choices=BOOL_CHOICES)
#     class Meta:
        
#         verbose_name = "Дополнительное письмо"
#         verbose_name_plural = "Дополнительные письма"
#         default_related_name = 'Additionalletters_files'

#     def __str__(self):
#             return str(self.name)[0:100]


        
# class NewsLine(models.Model):
    
#     datenews = models.DateField(verbose_name="Дата")
#     author = models.ForeignKey(FNSUser,on_delete=models.PROTECT, verbose_name="Автор",null=True,blank=True)
#     newstext = RichTextUploadingField(verbose_name="Текст новости")
#     urgency = models.BooleanField(verbose_name="Срочность", default=False)
#     statistictype = models.CharField(max_length=3, choices=Statname, default="FB1", verbose_name="Раздел")
#     shown = models.BooleanField(verbose_name="Видимость", default=True)
    
    
#     def __str__(self):
#         return str(self.datenews)
    

#     class Meta:
#         verbose_name = "Новостная лента для ФБ"
#         verbose_name_plural = "Новости"

# class NewslineFiles(models.Model):
#     name = models.CharField(verbose_name="Название", max_length=1000)
#     attachmentfile = models.FileField(verbose_name="Файл",upload_to="docfiles/%Y/%m/%d")
#     dock = models.ForeignKey(NewsLine, on_delete=models.CASCADE, null=True, related_name='news_files')
#     class Meta:
        
#         verbose_name = "Файл новости"
#         verbose_name_plural = "Файлы новостей"
#         default_related_name = 'newsline_files'

#     def __str__(self):
#             return str(self.name)[0:100]
        
# class FAQ(models.Model):    
#     order = models.IntegerField(verbose_name="Номер", blank=True, null=True)
#     question = models.CharField(verbose_name="Вопрос", max_length=500)
#     answer = RichTextUploadingField(verbose_name="Ответ")
#     statistictype = models.CharField(max_length=3, choices=Statname, default="FB1", verbose_name="Раздел")
#     shown = models.BooleanField(verbose_name="Видимость", default=True)
    
#     def __str__(self):
#         return self.question

#     class Meta:
#         verbose_name = "Частые вопросы"
#         verbose_name_plural = "Частые вопросы"




# @receiver(post_save, sender=ListDataFBone)

# def print_only_after_q_created(sender, instance, created, **kwargs):
  
#     if created:
#         layer = get_channel_layer()            
#         upload= ListDataFBone.objects.latest('date_unloading').date_unloading           
#         async_to_sync(layer.group_send)(
#         'informer',
#         {
#             'type': 'chat_message',
#             'message': {'upload': upload.strftime("%Y-%m-%d")
#         }}
        
#         )
    
    