from django.shortcuts import render
from django.db.models import Count,Q, Max
from numpy import NaN
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from statistic.models import *
import pandas as pd
import json
from statistic.helper import passportoff
from functools import reduce
import operator
from watcher.views import ServiceWatch

# Create your views here.
def calculate(dfr, deleter):
    
    dfr.loc[:,'Total'] = dfr.sum(numeric_only=True, axis=1)
    dfr['corrected'] = 0
   
    
    for i, row in dfr.iterrows():
        if i>0:            
            dfr.loc[i, 'corrected'] = dfr['Total'][i-1]-dfr['countDataOld'][i]
            if dfr.loc[i, 'corrected'] <0:
                dfr.loc[i, 'corrected'] = ''
        
    if deleter:
        dfr = dfr.iloc[1: , :]
    
    dfr=dfr.to_dict('records')      
    
    return dfr
class Dashboard(APIView):
    permission_classes = (AllowAny,)
    def get(self,request):
        ServiceWatch(request)
        
        try:
            filters = json.loads(self.request.query_params.get('filters'))          
            
        except TypeError:
            filters = {}
        
        max_date = ListDataFBone.objects.filter(date_unloading__lte=filters['date_unloading__lte']).aggregate(Max('date_unloading'))['date_unloading__max']
        
        group = ['passport__code', 'passport__name']
        filtercount = [Q(date_unloading__lte=max_date)]
        filtercount2=[Q(date_unloading=max_date)]
        
        # if request.user.region:
        #     filtercount.append(Q(region=request.user.region))
        if 'region__name__in' in filters.keys():            
            filtercount.append(Q(region__name__in=filters['region__name__in']))

        

        countData = Count('id_error', filter=(Q(*filtercount)))     
        
        exclude = passportoff() 
        if len(exclude)>0:
            toppassports = list(ListDataFBone.objects        
            .filter(date_unloading=max_date).exclude(reduce(operator.or_, exclude))
            .values(group[0], group[1])
            .annotate(countData=countData)
            .order_by('-countData')[:10] )
        else:
            toppassports = list(ListDataFBone.objects        
            .filter(date_unloading=max_date)
            .values(group[0], group[1])
            .annotate(countData=countData)
            .order_by('-countData')[:10] )

        group = ['region']


        filtercount2=[Q(date_unloading=max_date)]
        if "passport__code__in" in filters.keys(): 
           
            filtercount2.append(Q(passport__code__in=filters["passport__code__in"]))
            filtercount.append(Q(passport__code__in=filters["passport__code__in"]))
            
        
        countData = Count('id_error', filter=Q(*filtercount2))         
        if len(exclude)>0:
            topregion = list(ListDataFBone.objects
            .filter(date_unloading=max_date).exclude(reduce(operator.or_, exclude))
            .values(group[0], 'region__tax_code','region__name')
            .annotate(countData=countData)
            .order_by('-countData')[:10] )
        else:
            topregion = list(ListDataFBone.objects
            .filter(date_unloading=max_date)
            .values(group[0], 'region__tax_code','region__name')
            .annotate(countData=countData)
            .order_by('-countData')[:10] )

        group=['type_error']
        # totalerrormaxdate =list(ListDataFBone.objects
        # .filter(date_unloading=max_date).values(*group).annotate(countData=countData))

        # linear_tendention = list(ListDataFBone.objects.filter(date_unloading__lte=max_date, date_unloading__gte=filters['date_unloading__gte']).values('date_unloading').annotate(countData=countData).order_by('date_unloading'))
        # filtercount.append(Q(type_error=1))
        
        group=['date_unloading']  
        # "1 - Старая , 2 - Новая, 3 - ВПНД"
        
        ldbgte_1=ListDataFBone.objects.filter(date_unloading__gt="1900-01-01",date_unloading__lt=filters['date_unloading__gte']).distinct().order_by('-date_unloading').values('date_unloading').first()
        deleter=True
        if ldbgte_1 is not None:        
            ldbgte_1result=ldbgte_1['date_unloading']  
        else:
            ldbgte_1result= filters['date_unloading__gte']
            deleter=False

        if len(exclude):
            totalerrorperiod=pd.DataFrame(list(ListDataFBone.objects
            .filter(date_unloading__lte=max_date, date_unloading__gte=ldbgte_1result).exclude(reduce(operator.or_, exclude))
            .values(*group)
            .annotate(countDataOld=Count('id_error', filter=(Q(*filtercount) & Q(type_error=1))) )
            .annotate(countDataNew=Count('id_error', filter=(Q(*filtercount) & Q(type_error=2) )) )
            .annotate(countDataVPND=Count('id_error', filter=(Q(*filtercount) & Q(type_error=3))) )
            ))
        else:
             totalerrorperiod=pd.DataFrame(list(ListDataFBone.objects
            .filter(date_unloading__lte=max_date, date_unloading__gte=ldbgte_1result)
            .values(*group)
            .annotate(countDataOld=Count('id_error', filter=(Q(*filtercount) & Q(type_error=1))) )
            .annotate(countDataNew=Count('id_error', filter=(Q(*filtercount) & Q(type_error=2) )) )
            .annotate(countDataVPND=Count('id_error', filter=(Q(*filtercount) & Q(type_error=3))) )
            ))


        totalerrorperiod=calculate(totalerrorperiod, deleter) 
        
        
        
        
        
        
        return Response({'toppassportserrors':toppassports,'topregionserrors':topregion,'totalerrorperiod':totalerrorperiod, "max_date":max_date})