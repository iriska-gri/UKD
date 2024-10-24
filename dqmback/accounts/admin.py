from django.contrib import admin
from .models import FNSUser, Initial, Permission, Usergroup
from statistic.admin import BaseModelAdmin


class InitalAdmin(BaseModelAdmin):
    search_fields=('last_name', 'first_name','region__tax_code','permission__name',)
    list_display = ('last_name', 'first_name', 'middle_name','regionfn','regionname','permission',)
    fields=('last_name', 'first_name', 'middle_name','region','permission',)
    def regionname(self,obj):
        return obj.region.name if obj.region else ''
    def regionfn(self, obj):              
        return  obj.region.tax_code if obj.region else ''

    regionname.admin_order_field  = 'region__name'    
    regionname.short_description = "Регион"
    regionfn.admin_order_field  = 'region__tax_code'    
    regionfn.short_description = "Код региона"

class FNSUserAdmin(BaseModelAdmin):
    search_fields=('username','last_name', 'first_name','region__tax_code',)
    list_editable=("permission",)
    list_display = ('username','last_name', 'first_name', 'middle_name','regionfn','regionname',"permission",'is_superuser','is_staff')
    exclude =("email",'group','user_permissions','groups','password',) 

    fields=('username','last_name', 'first_name', 'middle_name','ip_client',"permission",'phone','lotus','region', 'is_superuser','is_staff', 'last_login','date_joined')  
    readonly_fields = ('last_login','date_joined','password','ip_client',) 


    def regionname(self,obj):
        return obj.region.name if obj.region else ''
    def regionfn(self, obj):              
        return  obj.region.tax_code if obj.region else ''
    regionname.admin_order_field  = 'region__name'    
    regionname.short_description = "Регион"
    regionfn.admin_order_field  = 'region__tax_code'    
    regionfn.short_description = "Код региона"

    # is_superusers.short_description = 'Вопрос задал'
admin.site.register(Permission)

admin.site.register(Usergroup)
admin.site.register(FNSUser, FNSUserAdmin)
admin.site.register(Initial, InitalAdmin)


# Register your models here.
