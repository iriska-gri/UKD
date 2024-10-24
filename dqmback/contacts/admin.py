from cProfile import label
from distutils import filelist
from re import L
from time import sleep
from django.contrib import admin
from .models import *
from django.http import HttpResponseRedirect
from datetime import datetime
from statistic.admin import BaseModelAdmin
import requests, os
from django.urls import path
from django import forms
import time
# Register your models here.


class CustomMetodolog(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return  f'{obj.first_name} {obj.middle_name}  {obj.last_name}'
class CustomPasspcode(forms.ModelMultipleChoiceField):
    template_name = 'templates/admin/multiple_input.html'
    def label_from_instance(self, obj):
        return  f'{obj.code}'

class MySPMA(forms.ModelForm):
    methodolog = CustomMetodolog(queryset=FNSUser.objects.filter(region__isnull=True),label='ФИО Методолога')
    connectedPassport = forms.ModelMultipleChoiceField(queryset=Passport.objects.all().order_by("code"), label="Коды паспортов",
    widget=forms.CheckboxSelectMultiple(
            attrs={
            
                "class": "column-checkbox"
            }
        ),
        required=False,
      
    )
    
   
    
    
    
    class Meta:
          model = SupportPassportMetodolog
          fields=['methodolog','connectedPassport'] 


          
class SupportPassportMetodologAdmin(admin.ModelAdmin):
    
    list_display= ("methodologname",'metphone',"connectedPassports")
    form = MySPMA
    
    def methodologname(self,obj):
        return  f'{obj.methodolog.first_name} {obj.methodolog.middle_name}  {obj.methodolog.last_name}'
    def metphone(self,obj):
        return f'{obj.methodolog.phone if obj.methodolog.phone else "Не указан"}'

    def connectedPassports(self,obj):
        return ",  ".join([p.code for p in obj.connectedPassport.all()])
        
    methodologname.short_description = 'ФИО Методолога'
    metphone.short_description = 'Телефон'
    connectedPassports.short_description = 'Паспорта'



class Questionfilesinline(admin.StackedInline):
    model = QuestionFiles
    extra = 0


class QuestionsAdmin(BaseModelAdmin):
    # change_form_template = "admin/change_form.html"
    list_display= ("questiondate",'questionshort',"status", 'readed', 'readersn','readedtime') 
    exclude =('asker',"answerer", 'last_reader',)
    readonly_fields = ('askername', 'otus', "questiondate",'question','answerdate', 'status','readed','readersn','readedtime',) 
    inlines = [Questionfilesinline]
    
    def otus(self, obj):
        return obj.asker.lotus
    def askername(self, obj):
        return f'{obj.asker.first_name} {obj.asker.middle_name}  {obj.asker.last_name}'

    def readersn(self, obj):
        try:
            return f'{obj.last_reader.last_name}'
        except Exception:
            return "-"

    def questionshort(self, obj):
        return str(obj.question)[0:50] +'...'
    # .save_related(self, request, form, formsets, change)
    
    def response_change(self, request, obj):
        if "_sendlotus" in request.POST:
            
            filelists = QuestionFiles.objects.filter(quest=obj.pk)
            filess=[]
            for x in filelists:                
                filess.append(('attachments',open(os.path.join("media",str(x.attachmentfile)), 'rb')))

            data = {'sendto':[obj.asker.lotus], 'subject':f'Ответ на ваш вопрос {obj.question}','body_text': obj.answer }
            resp =requests.post('http://10.252.44.13:8005/', data=data ,files=filess)
           
            if int(resp.status_code)==200:
                obj.status=True
                obj.answerer = request.user
                obj.answerdate = datetime.now()
                obj.save()
                
                return HttpResponseRedirect("admin/contacts/questions/")

        return super().response_change(request, obj)

    
        

    def save_model(self, request, obj, form, change):        
        if len(str(obj.answer))>0:
          
            obj.save()
            

           
            

        
    otus.short_description = "Ответ на адрес"
    readersn.short_description = 'Просматривал'
    askername.short_description = 'Вопрос задал'
    questionshort.short_description = 'Короткий текст вопроса'

admin.site.register(Contacts, BaseModelAdmin)
admin.site.register(Questions,QuestionsAdmin)
# admin.site.register(Adress)
admin.site.register(SupportPassportMetodolog,SupportPassportMetodologAdmin)
