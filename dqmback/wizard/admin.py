from django.contrib import admin
from django.conf import settings
from .models import *
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
)

class BaseModelAdmin(admin.ModelAdmin):
    list_per_page = settings.LIST_PER_PAGE

class Imagesinline(admin.StackedInline):
    model = Step.images.through
    extra=0
    verbose_name = "Картинка"
    verbose_name_plural = "Картинки"
    
class ActionsInline(admin.StackedInline):
    model = Step.actions.through
    extra=0
    fk_name = "stepnow"
    verbose_name = "Действие"
    verbose_name_plural = "Действия"

class StepAdmin(BaseModelAdmin):
    list_display= ('id','passport','name', 'numberstep') 
    list_editable=('numberstep',)   
    ordering = ('numberstep',)
    exclude = ('images',)
    inlines = [Imagesinline, ActionsInline]
 

    list_filter = (         
              ('passport', RelatedDropdownFilter),
            #   ('name', DropdownFilter),
    )

class WayAdmin(BaseModelAdmin):
    list_display= ('id','waystep')





# class PassportStepAdmin(BaseModelAdmin):
#     list_display= ('passport', 'step', 'button', 'numberstep','nextstep')
#     list_editable=('step','numberstep','nextstep','button')
#     ordering = ('numberstep',)
#     list_filter = (         
#               ('passport', RelatedDropdownFilter),
#               ('step', RelatedDropdownFilter),
#     )
    
admin.site.register(Step, StepAdmin)
# admin.site.register(PassportStep, PassportStepAdmin)

admin.site.register(Images, BaseModelAdmin)
admin.site.register(Way, WayAdmin)



