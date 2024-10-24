# from django.contrib.admin import SimpleListFilter
# from django.db.models import F, Func, Value
# import holidays
# import datetime

# def autoadminholliday(year):

#     date = datetime.date(year, 1, 1)
#     rus_holidays = holidays.RUS() 
#     weekends = []        
#     while year == date.year:            
#         if date.weekday() in [5 ,6] or date in rus_holidays: # Проверка на субботу и воскресеьне
#             weekends.append(date)   

#         date += datetime.timedelta(days=1)
#     return weekends

# class WeekdayFilter(SimpleListFilter):
#     title = 'День недели' 
#     parameter_name = 'date_of_holliday'

#     def lookups(self, request, model_admin):
#         wd= set([c.date_of_holliday.weekday() for c in model_admin.model.objects.all()])
      
#         dd=["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье",]
#         return   [(c,dd[c]) for c in wd] 
 
#     def queryset(self, request, queryset):
       
#         if self.value():
#             a= queryset.filter(date_of_holliday__iso_week_day = int(self.value())+1)
#             return a