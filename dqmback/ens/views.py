
from tracemalloc import Statistic
from warnings import filters
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
import re

from django.db.models import Count, Q
from django.db import transaction

import pandas as pd
import datetime
import os, shutil
import json
from accounts.models import FNSUser
from excelcreator.fb1 import createExcel
from django.core.files.storage import FileSystemStorage
from .models import *
from .serializers import *
from functools import reduce
import operator
from .helper import passportoff
from programlistener.helper import listfb1_deleted
from watcher.views import ServiceWatch
# from .helper import calculate_deadline

# def fio(name):
#     return f'{name}__'
type_error_dict={    
    'Старые НД':1,
    'Новые НД':2,
    'ВПНД':3
}




def clearfolder(folder):        
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
           
            pass

class PassportView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PassportSerializer
    queryset = Passport.objects.all().order_by('code')
   
    pagination_class = None
    def get(self, request):
        ServiceWatch(self.request)
        queryset = Passport.objects.all().order_by('code')
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


    def post(self, request):
        ServiceWatch(self.request)
        for name in ['algorithm_creation_period','selection_aproval_period','date_of_formation_of_the_initial_list', 'count_into_the_initial_list']:
            if request.data['data'][name] == '':
                request.data['data'][name] = None
        
        serializer = self.serializer_class(data=request.data['data'])
       

        if serializer.is_valid():
            
            serializer.method = request.data['method']
            serializer.datasbs =  request.data['data']['sub_system']
            serializer.save()
            try:
                serializer.save()
               
            except Exception as e:
                if request.data['method'] == 'add':
                    if str(e) != 'Паспорт с таким именем уже существует':
                        Passport.objects.filter(code = request.data['data']['code']).delete()
                return Response(status=201, data={'error': str(e)})
        else:
            e = str(serializer.errors)
           
            return Response(status=201, data={'error': str(serializer.errors)})
        return Response(status=201)


class PassportDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk):
       
        passport = Passport.objects.get(id=pk)
        serializer = PassportDetailSerializer(passport)
        return Response(serializer.data)


class ListDataFBoneView(ListAPIView):

    serializer_class = ListDataFBoneSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        ServiceWatch(self.request)
        filters={}
        try:
            filters = json.loads(self.request.query_params.get('filters'))
            
            nowsort = self.request.query_params.get('sort')

        except TypeError:
            filters = {}
       
        
        if self.request.user.region:
            filters['region__name__in']=[self.request.user.region.name]
        if nowsort in ['inn','-inn', 'ogrn','-ogrn','fid','-fid','-passport__code','passport__code','nocode','rocode','-nocode','-rocode']:
            data= customordering(ListDataFBone.objects.filter(**filters).all().order_by(nowsort).values('id','date_unloading','passport_id','fid','inn','ogrn','id_error','type_error','region_id','region__name','region__tax_code', 'passport__name', 'passport__code','nocode','rocode'), nowsort)
            # Отсечка первоначальной .filter(date_unloading__gt = "1900-01-01")
            return data

        return list(ListDataFBone.objects.filter(**filters).order_by(nowsort).values('id','date_unloading','passport_id','fid','inn','ogrn','id_error','type_error','region_id','region__name','region__tax_code', 'passport__name', 'passport__code','nocode','rocode'))

    def post(self, request):

        try:
            filters = json.loads(request.data['params']['filters'])
            
            nowsort = request.data['params']['sort']
            
        except TypeError:
            filters = {}        
        if self.request.user.region:
            filters['region__name__in']=[self.request.user.region.name]       
        
        data = customordering(ListDataFBone.objects.filter(**filters).order_by(nowsort).values('date_unloading', 'region__tax_code', 'region__name','nocode','rocode', 'passport__code', 'ogrn', 'inn', 'fid', 'type_error'),nowsort)
        
        if len(data):        
           
            
            fname = createExcel(data,request.data['params']['headers_table'], f"{request.data['params']['fn_modificator']}_за_{datesplitter(filters['date_unloading__in'])}", userid=request.user.id, types='ListDataFBoneView')
            return Response(status=200, data={'name':fname})
        return Response(status=200, data={'error':True})
        
def datesplitter(arr):
   
    res=""
    for x in arr:
        x = list(reversed(x.split("-")))
       
        res=res+"-".join(x)
   
    return res


def customordering(data, orderby):
   
    isDesc=True if orderby[0]=="-" else False
    if orderby in ['-passport__code','passport__code']:
        data= sorted(list(data),key=passport__codeSort,reverse=isDesc)
    elif orderby in ['-inn','inn']:
        data= sorted(list(data),key=innSort,reverse=isDesc)
    elif  orderby in ['ogrn','-ogrn']:
        data= sorted(list(data),key=ogrnSort,reverse=isDesc)
    elif  orderby in ['fid','-fid']:
        data= sorted(list(data),key=fidSort,reverse=isDesc)
    elif  orderby in ['nocode','-nocode']:
        data= sorted(list(data),key=nocodeSort,reverse=isDesc)
    elif  orderby in ['rocode','-rocode']:
        data= sorted(list(data),key=rocodeSort,reverse=isDesc)
    elif orderby in ['growth','-growth']:        
        data= sorted(list(data),key=growthSort,reverse=isDesc) 
    
    else:
        
        return data
    return data

def passport__codeSort(z):  
   
    x= z['passport__code']
    x=re.sub(r'[\s_a-zA-Zа-яА-ЯёЁ]',"",str(x))    
    y=x.split(".")
    y=y[0] +"."+ "".join(y[1:])    
    return (float(y))

def innSort(z):
    x= z['inn']
    return int(x) if len(str(x)) else 0
def ogrnSort(z):
    x= z['ogrn']
    return int(x) if len(str(x)) else 0
def fidSort(z):
    x= z['fid']
    return int(x) if len(str(x)) else 0
def rocodeSort(z):
    x= z['rocode']
    return int(x) if len(str(x)) else 0
def nocodeSort(z):
    x= z['nocode']
    return int(x) if len(str(x)) else 0
def growthSort(z):
    x= z['growth']
    

    return float(x) if len(str(x)) else 0
  

class MonitoringDataFBoneView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        ServiceWatch(request)
        filters=request.data['filters']
        
        if request.data['ifns'] and 'type_error' in filters:            
                    filters['type_error'] = type_error_dict[filters['type_error']]
        try:
            dates = filters['date_unloading__in']        
        except Exception:
            from django.db.models import Avg, Max, Min
            dates = ListDataFBone.objects.all().values_list('date_unloading').distinct().order_by('date_unloading')            
            dates = [dates[0][0], dates[len(dates)-1][0]]
        
        group = ['passport__code', 'passport__name'] if request.data['group_by']  else ['region__tax_code', 'region__name']
        if request.data['ifns'] and not request.data['group_by']:
            group = ['region__tax_code','region__name','nocode', 'rocode'] 
        countData = Count('id_error', filter=Q(date_unloading=dates[0]))
        # countData = Count('id_error', filter=Q(date_unloading=None))
        countCompare = Count('id_error', filter=Q(date_unloading=dates[1]))
        presort = request.data["sort"]["group_by"]
        
        sortd = group[0]
        if presort in ['percentage','growth']:
            presort=group[0]
            sortd = 'region__tax_code'
            presort = [f'{"-" if request.data["sort"]["desc"] else ""}{presort}']
        elif presort in ['countCompare']:
            presort =  ['-countCompare','region__tax_code']
            sortd = '-'
            # [f'{"" if request.data["sort"]["desc"] else "-"}{presort}']
           
        else:
            presort = [f'{"" if request.data["sort"]["desc"] else "-"}{presort}']
            sortd = 'region__tax_code'
        # print(presort, group,"---!!!!_----")
        if  request.data['ifns'] and self.request.user.region:
           filters['region__name__in']=[self.request.user.region.name]       
        
            # reduce(lambda x, y: x | y, [Q(brand=item) for item in brands]
        exclude = passportoff()
        
        if len(exclude)>0:
            data = customordering(list(ListDataFBone.objects.exclude(reduce(operator.or_, exclude))
            .filter(Q(**filters))
            .values(*group)
            .annotate(countData=countData, countCompare=countCompare)
            .order_by(*presort)), sortd) 

        else:
           
            data = customordering(list(ListDataFBone.objects
            .filter(Q(**filters))
            .values(*group)
            .annotate(countData=countData, countCompare=countCompare)
            .order_by(*presort)), sortd) 

        # print(data)
       

     
        if 'region__tax_code' in presort and 'region__name__in' not in filters.keys():
            allregions = list(Region.objects.all().values("tax_code",'name'))
            for x in allregions:
                d=next((d for d in data if d.get('region__tax_code')==x['tax_code']),None)
                if not d:
                    data.append({'region__tax_code': x['tax_code'], 'region__name': x['name'], 'countData': 0, 'countCompare': 0})
      
        # a = M.objects.filter(Q(f__isnull=True) | Q(f__in=['1',...])) 
        
        data = [self.countValue(x) for x in data]
       
        if 'percentage' in request.data["sort"]["group_by"]:           
        
            data.sort(key=lambda d: d['percentage'],reverse= not request.data["sort"]["desc"])

        elif 'growth' in request.data["sort"]["group_by"]:            
            data = customordering(data,f'{"" if request.data["sort"]["desc"] else "-"}{request.data["sort"]["group_by"]}')

        if 'excel' in request.data: 
            if len(data):
                     
                fname= createExcel(data,request.data['headers_table'],namen=f"{request.data['fn_modificator']}_{datesplitter([filters['date_unloading__in'][0]])}_и_{datesplitter([filters['date_unloading__in'][1]])}",userid=request.user.id)
                return Response(status=200, data={'name': fname})
            return Response(status=200, data={'error': 'Не найдено записей'})

        
        return Response(status=200, data=data)

    def countValue(self, x):
        x['growth'] = x['countCompare'] - x['countData']
        
        x['percentage'] = round(x['growth']/x['countData']*100, 2) if x['countData'] != 0 else 100
        
        
        if x['countCompare']==0 and x['countData']==0:
            x['percentage'] = -100

        return x

class MonitoringDataForModal(APIView):
    # IsAuthenticated,
    permission_classes = (AllowAny,)
    def post(self, request):
        pass
        return Response(status=200, data=[])





# class FileUploadView(APIView):
    
#     permission_classes = (IsAuthenticated,)
#     """ Принимает файл на сервере в параметре attr нужно указать функцию обработчик, в file - файл """
    
#     # permission_classes = (IsAuthenticated, )
#     @transaction.atomic
#     def put(self, request):
        
#         try:
#             clearfolder(os.path.join('media','media','uploads','FB1'))
#             # result=getattr(self, request.data.get('attr'))(request.data.get('file'))
#             fs = FileSystemStorage()
#             file=request.data.get('file')
#             filepath=os.path.join('media','uploads',request.data.get('attr'), 'uploads.xlsx')
#             file = fs.save(filepath, file)
        
#         except FileNotFoundError:
#             return Response(status=200, data={'msg': 'Выберите файл'})
#         # except Exception:
#         #     return Response(status=200, data={'msg': 'Неизвестная ошибка'})

#         return Response(status=200, data={'filepath':filepath, 'attr': request.data.get('attr')})
            
#     def post(self, request):
#         filters=json.loads(request.data['params']['filters'])
        
#         ListDataFBone.objects.filter(**filters).delete()
#         listfb1_deleted()
#         return Response(status=200, data="ok")
    
# class DocksData(APIView):
#     permission_classes = (IsAuthenticated,) 


#     def get(self, request, statistictype): 
     
        
#         docs,news=[],[]
#         try:    
#             newsQ = NewsLine.objects.filter(statistictype= statistictype.upper(), shown=True, datenews__lte=datetime.date.today()).prefetch_related('news_files').order_by('-datenews')
            
#             for x in newsQ:           
#                 n={
                        
#                         "datenews": x.datenews,
#                         # "author__first_name":x.author.first_name,
#                         # "author__last_name":x.author.last_name,
#                         # "author__middle_name":x.author.middle_name,
#                         "newstext":x.newstext,
#                         'news_files':[]
#                 }
                
#                 for s in x.news_files.all():                   
#                     n["news_files"].append({"file":str(s.attachmentfile), "doc":str(s.name)})
#                 news.append(n)



#         except Exception as e:
            
#             pass
#         try: 
#             fq = list(FAQ.objects.filter(statistictype= statistictype.upper(), shown=True).order_by("order").values("pk","order" ,"question", "answer"))
#         except Exception:
#             pass
#         try: 
#             docsandfQuery = Documentation.objects.filter(statistictype= statistictype.upper()).prefetch_related('document_files', 'addition_files')
            
#             docs = {"doc": docsandfQuery[0].doc,
#                     "statistictype":docsandfQuery[0].statistictype,
#                     "file": str(docsandfQuery[0].file),
#                     "attachments":[],
#                     'additions':[],
#                     'contactinfo':[]}
#             helper={'True':'additions', 'False':'contactinfo'}
#             for s in docsandfQuery[0].document_files.all():
#                 docs["attachments"].append({"doc":str(s.name),"file":str(s.attachmentfile)}) 
#             for s in docsandfQuery[0].addition_files.all():                
#                     docs[helper[str(s.typin)]].append({"doc":str(s.name), "file":str(s.attachmentfile),'typin':s.typin})   
                         
                      
#         except Exception:
#             pass

#         return Response({
#                         "docs":docs,
#                         "faq":fq,
#                          "news":news
#                          }) 

    
# class GetDynamics(ListAPIView):
#     serializer_class = DinamicSerializer
#     permission_classes = (IsAuthenticated,)
#     def get_queryset(self):        
#         try:
#             filters = json.loads(self.request.query_params.get('filters')) 
#         except TypeError:
#             filters={}
        
#         # return Response(self.objectgood(list(Dynamics.objects.filter(**filters).order_by('name'))))
#         return list(Dynamics.objects.filter(**filters).order_by('-date_unloading','name'))
    
#     def post(self, request):
#         from pathlib import Path
#         files = request.FILES.getlist('files[]')
#         dateunl = request.data.get('date_unloading')
#         for file in files:
#             path = Path(file.name)            
#             Dynamics.objects.create(date_unloading=dateunl, name=path.stem, file=file)

#         return Response({"mess":"Файлы загружены"})

from django.shortcuts import render
from django.db.models import Count,Q, Max
from numpy import NaN
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

import pandas as pd
import json
from statistic.helper import passportoff
from functools import reduce
import operator

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