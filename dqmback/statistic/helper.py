import datetime
from collections import Counter
from pickle import TRUE # Для сравнения списков 04.04.2022 I
import holidays
from numpy import number
from accounts.models import FNSUser
from statistic.models import PassportOff
from django.db.models import Count, Q
# from accounts.models import FNSUser
 # Праздничный календарь на год

def sortFilterForData(filters):
    
    filt = {}

    for key in filters:

        prefix = '__in' if type(filters[key]) == list else ''
        filt[f'{key}{prefix}'] = filters[key]
        
    return filt



def calculate_deadline(hol,reasondays,justifydate):     
    weekends = []
    for x in hol:
        weekends.append(x["date_of_holliday"])
    i=0
    while i < reasondays+1:
        justifydate += datetime.timedelta(days=1)
        if justifydate not in weekends:
            i+=1
        
    return justifydate


def shname(id):
    chel = FNSUser.objects.get(pk=id)
    return f'{chel.last_name[0]} {chel.first_name[0]}.{chel.middle_name[0]}.'


def passportoff():
    passportoff = list(PassportOff.objects.all().values("passport","datefrom","dateto","type_error"))      

    passportoffFilter = []
    for x in passportoff:
        xfil=''
        if x['dateto'] is not None :
            xfil = Q(passport=x['passport'], date_unloading__gte=x['datefrom'],date_unloading__lte=x['dateto'], type_error=x['type_error'])
        else:
            xfil = Q(passport=x['passport'], date_unloading__gte=x['datefrom'],type_error=x['type_error'])
        passportoffFilter.append(xfil)
        
    return passportoffFilter