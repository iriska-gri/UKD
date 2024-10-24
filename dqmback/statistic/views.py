
from tracemalloc import Statistic
from warnings import filters
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
import re
from ens.models import SubSystem as ensSubS
from ens.models import ListDataFBone as LDFBO
from ens.models import Passport as ensPASS
from django.db.models import Count, Q
from django.db import transaction

import pandas as pd
import datetime
import os, shutil
import json
from accounts.models import FNSUser
from excelcreator.fb1 import createExcel
from django.core.files.storage import FileSystemStorage
from .models import JustifyFiles, PassportOff, Region, ListDataFBone, Passport, ReasonForNotNormalizing, Justify, SubSystem, Priority, Criticality, ResponsibleMonitoring, NewsLine, FAQ,Documentation, Dynamics
from .serializers import ListDataFBoneSerializer, JustifyDataFBoneSerializer, PassportDetailSerializer, PassportSerializer, DinamicSerializer
from functools import reduce
import operator
from .helper import passportoff
from programlistener.helper import listfb1_deleted
from watcher.views import ServiceWatch
from watcher.models import Watcher
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
        # print("qqqqqqqqqqqqqqqqq")
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
   

class JustifyDataFBoneView(ListAPIView):

    serializer_class = JustifyDataFBoneSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        
        try:
            filters = json.loads(self.request.query_params.get('filters')) 
            filters2={}         
            nowsort = self.request.query_params.get('sort')
            
            # !Переделать это дерьмо
            if 'justify__fix_status__in' in filters.keys():                
                for x in range(len(filters['justify__fix_status__in'])):                   
                    if(filters['justify__fix_status__in'][x]=="Не согласовано"):                         
                        filters['justify__fix_status__in'][x]=False
                    elif(filters['justify__fix_status__in'][x]=="Согласовано"):
                        filters['justify__fix_status__in'][x]=True
                    elif(filters['justify__fix_status__in'][x]=="На согласовании"):
                        filters['justify__fix_status__in'][x]=None
                        filters2=filters.copy()
                        del filters2['justify__fix_status__in']
                        filters2['justify__fix_status__isnull']=True
        except TypeError:
            filters, filters2 = {},{}

            nowsort='pk'
           
        if self.request.user.region:
            filters['region__name__in']=[self.request.user.region.name]
        
        if 'justify__methodologist__in' in filters.keys():
            
            metodolog = []
            arrd=filters['justify__methodologist__in']
            
            filters['justify__methodologist__in']=[]
            for el in arrd:                
                sn = el.split(" ")                  
                a=list(FNSUser.objects.filter(region__isnull=True).filter(last_name=sn[0],first_name=sn[1], middle_name=sn[2]).values('id'))
                
                for x in a:
                    filters['justify__methodologist__in'].append(x['id'])    
            filters2['justify__methodologist__in']=filters['justify__methodologist__in']
      
        
        data=ListDataFBone.objects.filter(date_unloading__gt = "1900-01-01").filter(Q(**filters)|Q(**filters2)).all().order_by(nowsort).values('id','date_unloading', 'passport__code', 'passport__name','region__tax_code','region__name', 'justify__date_of_justification', 'ogrn', 'inn', 'fid','justify__description', 'justify__reason__name','justify__methodologist',  'justify__methodologist_note', 'justify__agreement_date', 'justify__fix_status','justify__pk' )
        
        return customordering(data, nowsort)


        
    def post(self, request):        
        
        try:
            filters = json.loads(request.data['params']['filters'])
            nowsort = request.data['params']['sort']
            fn_modificator = request.data['params']['fn_modificator'].replace(" ","_")
            
        except TypeError:
            filters = {}
        if self.request.user.region:
            filters['region__name__in']=[self.request.user.region.name]
        datefields=['date_unloading']
        values=['date_unloading', 'passport__code', 'region__tax_code',  'ogrn', 'inn', 'fid']
        if not filters["justify__reason__name__isnull"]:
            datefields =datefields+['justify__agreement_date']    
            values=values+['justify__reason__name', 'justify__fix_status', 'justify__agreement_date','justify__methodologist', 'justify__methodologist__last_name', 'justify__methodologist__first_name','justify__methodologist__middle_name']
        predata =list(ListDataFBone.objects.filter(**filters).order_by(nowsort).values(*values))
        if len(predata)> 1000000:
            return Response(status=200, data={'error': "*Доступно создание не более 1000000 записей"})
        elif len(predata)== 0:
            return Response(status=200, data={'error': 'Не найдено записей'})
        
        data = customordering(predata,nowsort)
        
        if not filters["justify__reason__name__isnull"]:
            for x in data:
                if x['justify__fix_status'] is not None:
                    x['justify__fix_status']= "Согласовано" if x['justify__fix_status'] else "Не согласовано"
                else:
                    x['justify__fix_status']= "На согласовании"
                x['justify__methodologist']=f"{x['justify__methodologist__last_name']} {x['justify__methodologist__first_name'][0]}. {x['justify__methodologist__middle_name'][0]}." if x['justify__methodologist'] is not None else None
        
           
        fname=  f'Исключения_{fn_modificator}.xlsx'   
        fname= createExcel(data, request.data['params']['headers_table'], request.data['params']['fn_modificator'],userid=request.user.id, types='JustifyDataFBoneView')
        
        return Response(status=200, data={'name': fname})
        

class CreateJustifyFBone(APIView):
    permission_classes = (IsAuthenticated,)
    
    def put(self, request):
        # newFiles = request.FILES.getlist('file')
        obj={}
        meth=""
        l = ListDataFBone(id=request.data['id'])
        fields = json.loads(request.data['fields'])
        if 'description' in fields.keys():
            obj['description']= fields['description']
            
        
# !ТУТ АПДЕЙТ
        if 'reason__name' in  fields.keys():
            reason = fields['reason__name']
            if reason:
                obj['reason'] = ReasonForNotNormalizing.objects.get(name=reason)
                meth="create"
        
        elif  'fix_status' in  fields.keys():
            meth="update"
            obj['fix_status']=fields['fix_status']
            obj['methodologist_note']=fields['methodologist_note']
            obj['methodologist']=FNSUser.objects.get(pk=request.user.id)
            obj['agreement_date']=datetime.date.today()
        




        j, created = Justify.objects.update_or_create(listdate=l, defaults=obj) 
        metodolog = True
        if created:
            metodolog=False
        fileattached=[]
        for file in request.FILES.getlist('file'):
            fileattached.append(JustifyFiles(file=file, author=metodolog, justif=Justify(id=j.id)))

            
        Qfiles= JustifyFiles.objects.bulk_create(fileattached)
        # if obj['reason'].perioddead:
        #         hol = list(Holliday.objects.filter(date_of_holliday__gte=j[0].date_of_justification).values("date_of_holliday"))                
        #         # j[0].deadline_for_correction = calculate_deadline(hol,obj['reason'].perioddead ,j[0].date_of_justification)               
        # else:
        #     j[0].deadline_for_correction =None
        # j[0].save()
        filespathes=[]
        for f in Qfiles:
            filespathes.append(str(f.file))

        data={}        
        if  meth=='update':
            data={'justify__agreement_date': j.agreement_date,
                  'justify__methodologist': f'{request.user.last_name} {request.user.first_name[0]}. {request.user.middle_name[0]}.' ,
                  'justify__justifiles': filespathes}
        return Response(status=200, data=data)


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


class GetFilters(APIView):
    """ Получение фильтров """
    
    dictModel = {
        'sub_system_ens':ensSubS,
        'ens':LDFBO,
        'ensPass':ensPASS,
        'listFB1': ListDataFBone,
        'regions': Region,
        'passports': Passport,
        'justify': Justify,
        'reason': ReasonForNotNormalizing,
        'sub_system': SubSystem, 
        'priority': Priority,
        'criticality': Criticality,
        'responsible': ResponsibleMonitoring,
        'dynamicdate': Dynamics,
        'watcher':Watcher,
        'watcher_regions':Watcher
        
    }

    def post(self, request):
        
        data = {}

        try:
            for (modelName, fields) in request.data.items():      
                print(modelName)      
                for field in fields:
                
                    if modelName == 'regions':
                        # if self.request.user.region:
                        #     filters={"pk":self.request.user.region.pk}
                        #     data['region__name'] = list(Region.objects.distinct().filter(**filters).order_by('tax_code').values_list('tax_code', 'name', ))
                        # else:
                        data['region__name'] = list(Region.objects.distinct().order_by('tax_code').values_list('tax_code', 'name', ))
                        continue
                    if modelName =='watcher_regions':
                        
                        data['user__region__name']= list(Watcher.objects.filter(user__is_staff=False, user__region__isnull=False).order_by('user__region__tax_code').values_list("user__region__tax_code","user__region__name"))
                       
                        data['user__region__name'].append(('00',"Центральный Аппарат",))
                        continue

                    name = field["related_name"] if "related_name" in field else field["name"]                    
                    notNull = {f'{name}__isnull': False}
                  
                    if field["sort"] != 'none':
                        sortField = f'{field["sort"]}' if len(field["sort"]) > 1 else f'{field["sort"]}{name}'
                        if field['name']=='date_unloading':                            
                            result = self.dictModel[modelName].objects.all().order_by(sortField).distinct().values_list(name, flat=True)
                        
                        elif name=='methodologist':                            
                            resulten = self.dictModel[modelName].objects.all().filter(methodologist__isnull=False).order_by(sortField).distinct().values_list(f'{name}__last_name', f'{name}__first_name',f'{name}__middle_name')
                            result=[]
                            
                            for el in resulten:                                
                                result.append(" ".join(el))
                                
                        elif name=="fix_status":
                            result=[True, False,None]       
                        else:
                            result = self.dictModel[modelName].objects.filter(**notNull).order_by(sortField).distinct().values_list(name, flat=True)
                    else:
                        result = self.dictModel[modelName].objects.filter(**notNull).distinct().values_list(name, flat=True)
                    
                    data[field["name"]] = list(result)
               
            
        except Exception as e:
            print(e)
            return Response(status=200, data={})
        # print(data)
        return Response(status=200, data=data)



class FileUploadView(APIView):
    
    permission_classes = (IsAuthenticated,)
    """ Принимает файл на сервере в параметре attr нужно указать функцию обработчик, в file - файл """
    
    # permission_classes = (IsAuthenticated, )
    @transaction.atomic
    def put(self, request):
        
        try:
            clearfolder(os.path.join('media','media','uploads','FB1'))
            # result=getattr(self, request.data.get('attr'))(request.data.get('file'))
            fs = FileSystemStorage()
            file=request.data.get('file')
            filepath=os.path.join('media','uploads',request.data.get('attr'), 'uploads.xlsx')
            file = fs.save(filepath, file)
        
        except FileNotFoundError:
            return Response(status=200, data={'msg': 'Выберите файл'})
        # except Exception:
        #     return Response(status=200, data={'msg': 'Неизвестная ошибка'})

        return Response(status=200, data={'filepath':filepath, 'attr': request.data.get('attr')})
            
    def post(self, request):
        filters=json.loads(request.data['params']['filters'])
        model = ListDataFBone
        if 'date_unloading__ens__in' in filters.keys():
            model = LDFBO
            filters['date_unloading__in']=filters['date_unloading__ens__in']
            del filters['date_unloading__ens__in']
        model.objects.filter(**filters).delete()
        listfb1_deleted()
        return Response(status=200, data="ok")
    
class DocksData(APIView):
    permission_classes = (IsAuthenticated,) 


    def get(self, request, statistictype): 
        ServiceWatch(request)
       
        docs,news=[],[]
        try:    
            newsQ = NewsLine.objects.filter(statistictype= statistictype.upper(), shown=True, datenews__lte=datetime.date.today()).prefetch_related('news_files').order_by('-datenews')
            
            for x in newsQ:           
                n={
                        
                        "datenews": x.datenews,
                        # "author__first_name":x.author.first_name,
                        # "author__last_name":x.author.last_name,
                        # "author__middle_name":x.author.middle_name,
                        "newstext":x.newstext,
                        'news_files':[]
                }
                
                for s in x.news_files.all():                   
                    n["news_files"].append({"file":str(s.attachmentfile), "doc":str(s.name)})
                news.append(n)



        except Exception as e:
            
            pass
        try: 
            faq = []
            fq = FAQ.objects.filter(statistictype= statistictype.upper(), shown=True).prefetch_related('faq_files').order_by("order")
            # .values("pk","order" ,"question", "answer",'faq_files'))
            # print(ggq)
            for x in fq:
                el= {
                    "pk": x.pk,
                    "order": x.order,
                    "question":x.question,
                    "answer":x.answer,

                }
                el["files"] = [{"doc":str(y.name),"file":str(y.attachmentfile)} for y in x.faq_files.all()]

                faq.append(el)
        except Exception:
            pass
        try: 
            docsandfQuery = Documentation.objects.filter(statistictype= statistictype.upper()).prefetch_related('document_files', 'addition_files')
            
            docs = {"doc": docsandfQuery[0].doc,
                    "statistictype":docsandfQuery[0].statistictype,
                    "file": str(docsandfQuery[0].file),
                    "attachments":[],
                    'additions':[],
                    'contactinfo':[]}
            helper={'True':'additions', 'False':'contactinfo'}
            for s in docsandfQuery[0].document_files.all():
                docs["attachments"].append({"doc":str(s.name),"file":str(s.attachmentfile)}) 
            for s in docsandfQuery[0].addition_files.all():                
                    docs[helper[str(s.typin)]].append({"doc":str(s.name), "file":str(s.attachmentfile),'typin':s.typin})   
                         
                      
        except Exception:
            pass
   
        return Response({
                        "docs":docs,
                        "faq":faq,
                         "news":news
                         }) 

    
class GetDynamics(ListAPIView):
    serializer_class = DinamicSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        ServiceWatch(self.request)        
        try:
            filters = json.loads(self.request.query_params.get('filters')) 
        except TypeError:
            filters={}
        
        # return Response(self.objectgood(list(Dynamics.objects.filter(**filters).order_by('name'))))
        return list(Dynamics.objects.filter(**filters).order_by('-date_unloading','name'))
    
    def post(self, request):
        from pathlib import Path
        files = request.FILES.getlist('files[]')
        dateunl = request.data.get('date_unloading')
        for file in files:
            path = Path(file.name)            
            Dynamics.objects.create(date_unloading=dateunl, name=path.stem, file=file)

        return Response({"mess":"Файлы загружены"})
