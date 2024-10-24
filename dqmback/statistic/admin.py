from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *
from accounts.models import *
from bs4 import BeautifulSoup
import re
# from .adminhelper import WeekdayFilter, autoadminholliday
from io import BytesIO
import locale
import datetime
from django.http import HttpResponseRedirect
from django.conf.urls import url
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
)
from import_export.admin import ExportActionMixin
from import_export import resources, fields
class BaseModelAdmin(admin.ModelAdmin):
    list_per_page = settings.LIST_PER_PAGE

class PersonResource(resources.ModelResource):

    class Meta:
        model = ListDataFBone
        fields = ('date_unloading', 'region', 'passport__code', 'fid', 'inn', 'id_error', 'type_error',)


class ListDataFBBoneAdmin(ExportActionMixin,BaseModelAdmin):
    # resource_classes  = resources('date_unloading', 'region', 'passport__code', 'fid', 'inn', 'id_error', 'type_error',)
    resource_class = PersonResource
    list_display = ('date_unloading', 'region', 'passport', 'fid', 'inn', 'id_error', 'type_error')
    list_filter = ( ('date_unloading', DropdownFilter),
        # for choice fields
              ('passport', RelatedDropdownFilter),
              ('region', RelatedDropdownFilter),
    )
class ReasonForNotNormalizingAdmin(BaseModelAdmin):
    pass
    # list_display = ('number', 'name', 'perioddead')
    # list_display_links = ('name',)
    # list_editable = ('number','perioddead')

class RegionList(BaseModelAdmin):
    list_display = ('tax_code', 'name')

class Newsfilesinline(admin.StackedInline):
    model = NewslineFiles
    extra = 0    

class Faqfilesinline(admin.StackedInline):
    model = FAQFiles
    extra = 0 

class NewsLineAdmin(BaseModelAdmin):
    inlines = [Newsfilesinline]
    exclude =("author",)
    # readonly_fields = ['author']
    list_display= ("datenews",'get_author',"short_text",'shown',"statistictype")    
    
    def get_author(self, obj):
        return f'{obj.author.first_name} {obj.author.last_name}'
    def short_text(self,obj):
        s= BeautifulSoup(obj.newstext)
        return s.get_text()[0:100] + "..."    
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.save()
    get_author.short_description = 'Автор'
    short_text.short_description = 'Короткий текст новости'
    

class FaqAdmin(BaseModelAdmin):
    inlines = [Faqfilesinline]
    list_display= ("question",'order',"shown", "statistictype") 
    list_editable = ('order',)   



class Docfilesinline(admin.StackedInline):
    model = DocumentationFiles
    classes = ['collapse']
    extra = 0
    
class DocAdditionsinline(admin.StackedInline):
    model = AdditionallettersFiles
    classes = ['collapse']
    extra = 0   
    
class DocumentationAdmin(BaseModelAdmin):
    list_display= ("docshort","statistictype")
    inlines = [Docfilesinline, DocAdditionsinline]
    
    def docshort(self,obj):
        return str(obj.doc)[0:100]

    
class PassportAdmin(BaseModelAdmin):
    list_display= ("code","name")
    
class PassportOffAdmin(BaseModelAdmin):
    list_display= ("passport", 'datefrom', 'dateto','type_error')

class JustifyFilesInline(admin.StackedInline):
    model = JustifyFiles
    extra = 0    

class JustifyAdmin(BaseModelAdmin):
    inlines = [JustifyFilesInline]
    readonly_fields = ('listdate',)


class DynamicsAdmin(BaseModelAdmin):
    list_display= ("date_unloading","name",)


# class HollidayAdmin(BaseModelAdmin):
#     change_list_template = "admin/model_change_list.html"
#     list_filter = (WeekdayFilter,)
#     list_display= ("date_of_holliday", "docshort")

#     def docshort(self,obj):
#         if settings.DEBUG:
#             locale.setlocale(locale.LC_ALL, ("RU"))
#         else:
#             locale.setlocale(locale.LC_ALL, ("RU", "UTF8"))
#         return obj.date_of_holliday.strftime("%A")
        
#     docshort.short_description = "День недели"

#     def get_urls(self):
#         urls = super(HollidayAdmin, self).get_urls()
#         custom_urls = [
#         url('^import/$', self.process_import, name='process_import'),]
#         return custom_urls + urls
#     def process_import(self, request):
#         hol = []
#         arrayofoutput = [] # Массив из выходных и праздников для заливки в базу
#         if request.FILES:
#             upload = request.FILES['upload']            
#             for line in upload:
#                 hol.append(re.sub("^\s+|\n|\r|\s+$", '', line.decode()))
                
#         elif request.POST["year"] != '':
#             hol = autoadminholliday(int(request.POST["year"]))
 
#         for x in hol:
#             arrayofoutput.append(Holliday(date_of_holliday = x))    
#         Holliday.objects.bulk_create(arrayofoutput, ignore_conflicts=True)

#         count = len(hol)-1
#         self.message_user(request, f"создано {count} новых записей")
#         return HttpResponseRedirect("../")


admin.site.register(Dynamics, DynamicsAdmin)
admin.site.register(Region,RegionList)
admin.site.register(Passport, PassportAdmin)
admin.site.register(PassportOff, PassportOffAdmin)
admin.site.register(ListDataFBone, ListDataFBBoneAdmin)
admin.site.register(Justify,JustifyAdmin)
admin.site.register(ReasonForNotNormalizing, ReasonForNotNormalizingAdmin)
admin.site.register(DescriptionData,BaseModelAdmin)
admin.site.register(Criticality,BaseModelAdmin)
admin.site.register(Priority,BaseModelAdmin)
admin.site.register(ResponsibleMonitoring)
admin.site.register(SubSystem,BaseModelAdmin)
admin.site.register(NewsLine, NewsLineAdmin)
admin.site.register(FAQ, FaqAdmin)
admin.site.register(Documentation, DocumentationAdmin)
# admin.site.register(Holliday,HollidayAdmin)


admin.site.unregister(Group)
admin.site.site_header = 'Панель администратора сайта УКД'
admin.site.site_title = 'Панель администратора сайта УКД'
