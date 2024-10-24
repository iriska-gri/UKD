from django.test import TestCase

# Create your tests here.
import datetime
from collections import Counter # Для сравнения списков 04.04.2022 I
import holidays # Праздничный календарь на год

# class Helper(APIView):
#     permission_classes = (AllowAny,)

    
#     def get(self,request):

# # Текущий год
#         year = [datetime.datetime.today().year, datetime.datetime.today().year+1]
#         weekends = []
#         for x in range(len(year)):
#             date = datetime.date(year[x], 1, 1) # начало года
#             z = 0
            

#     # Определяем количетсво дней в году
#             if (year[x] % 4 == 0 and year[x] % 100 != 0) or year[x] % 400 == 0:
#                 kdy = 365 # 366 дней
#             else:
#                 kdy = 364 # 365 дней

#     # Заполняем список выходными датами
#             while z < kdy:
#                 date += datetime.timedelta(days=1)
#                 z +=1
#                 if date.weekday() == 5 or date.weekday() == 6:
#                     weekends.append(date)
#                 else:
#                     pass

#     #Добавляем праздничные дни России
#             for p in holidays.RUS(years = year[x]).items(): 
#                 weekends.append(p[0]) 

# # Получаем даты из базы
#         doj = list(Justify.objects.distinct().order_by('date_of_justification').values("date_of_justification", "reason"))
#         for x in range(len(doj)): # Идет по строкам, по количеству записей
#             reason_id = doj[x]['reason'] 
#             oldholday = doj[x]['date_of_justification']
#             holday = doj[x]['date_of_justification']
#             if reason_id == 1:
#                 C += datetime.timedelta(days=2)
#             elif reason_id == 2:
#                 holday += datetime.timedelta(days=30)
#             elif reason_id == 3:
#                 holday += datetime.timedelta(days=10)
#             elif reason_id == 4:
#                 holday = holday
# # Выводим даты между датами
#             delta = holday - oldholday   # returns timedelta
#             beetwen = []
#             for i in range(delta.days + 1):
#                 day = oldholday +  datetime.timedelta(days=i)
#                 beetwen.append(day)



# # Считаем количество дней выходных, которые находятся между начальной и конечно датой
#             a = list((Counter(beetwen) & Counter(weekends)).elements())
#             # print(len(a))
#             newholday = holday + datetime.timedelta(days=len(a))
#             if newholday == oldholday:
#                 newholday = ''
#             # print(beetwen)
#             # print(oldholday, holday, newholday)
#         # return Response(doj)


# def calculate_deadline(hol,reasondays,justifydate):  
#     print('!!!!')  
#     print(hol)
#     # Текущий год
#     # year = [datetime.datetime.today().year, datetime.datetime.today().year+1]
#     rus_holidays = holidays.country_holidays('RU')
#     date = justifydate 
    
#     weekends = []
#     for x in range(150):
#         if date.weekday() in [5,6] or date in rus_holidays:
#             weekends.append(date)
#         date += datetime.timedelta(days=1)    
#     # print(weekends)
#     i=0
#     deadlineday=justifydate
#     while i < reasondays+1:
#         deadlineday += datetime.timedelta(days=1)
#         if deadlineday not in weekends:
#             i+=1
        
#     return deadlineday

    # if reason_id == 1:
    #     holday += datetime.timedelta(days=2)
    # elif reason_id == 2:
    #     holday += datetime.timedelta(days=30)
    # elif reason_id == 3:
    #     holday += datetime.timedelta(days=10)
    # elif reason_id == 4:
    #     holday = holday
            
