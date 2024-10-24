from dataclasses import replace
from re import L
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
import datetime
import re
from accounts.models import FNSUser
from statistic.models import *
from .serializers import ContactsSerializer,PassportMetodologSerializer
from django.db.models import Count, Q
# Create your views here.
from statistic.helper import passportoff
from functools import reduce
import operator
from django.views.generic import View, TemplateView

class Ipgetter(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        return Response ({"ip": request.META.get("HTTP_X_FORWARDED_FOR") })

class Mainpage(APIView):
    permission_classes = (AllowAny,)
    def get(self,request):
        
        FNSUser.objects.filter(id=request.user.id).update(ip_client=request.META.get("HTTP_X_FORWARDED_FOR"), last_login=datetime.datetime.now())
        
        news=[]
        filtercount = []
        if request.user.region:
            filtercount.append(Q(region=request.user.region))

        newsQ = NewsLine.objects.filter(shown=True, datenews__lte=datetime.date.today()).prefetch_related('news_files').order_by('-datenews')
        
        for x in newsQ:           
            n={                    
                    "datenews": x.datenews,
                    "author__first_name":x.author.first_name,
                    "author__last_name":x.author.last_name,
                    "author__middle_name":x.author.middle_name,
                    "newstext":x.newstext,
                    "urgency":x.urgency,
                    'news_files':[]
            }
            
            for s in x.news_files.all():                   
                n["news_files"].append({"file":str(s.attachmentfile), "doc":str(s.name)})
            news.append(n)
        # adress = list(FNSUser.objects.filter(region__isnull=True, is_superuser=False).order_by('last_name').values('first_name','middle_name','last_name','phone'))
        # cont= Contacts.objects.latest('pk')
        # serializer = ContactsSerializer(cont,context={"request": request})
        # metodologs = PassportMetodologSerializer(SupportPassportMetodolog.objects.all().order_by('methodolog__last_name'), many=True)
        # list(FNSUser.objects.filter(region__isnull=True, is_superuser=False).order_by('last_name').values('first_name','middle_name','last_name','phone'))
        group = ['passport__code','passport__name', 'date_unloading']
        countData = Count('id_error', filter=(Q(*filtercount))) 
        totalpassports = Passport.objects.all().count()
        exclude = passportoff()
        data = ListDataFBone.objects.filter(date_unloading__gt="1900-01-01")
        if len(exclude)>0:
            linear = list(data.exclude(reduce(operator.or_, exclude)).values(group[2]).annotate(countData=countData).order_by(group[2]))
        else:
            linear = list(data.values(group[2]).annotate(countData=countData).order_by(group[2]))




        max_date = ListDataFBone.objects.latest('date_unloading').date_unloading
        
        filtercount.append(Q(date_unloading=max_date))  
        if len(exclude)>0:            
            toppassports = list(ListDataFBone.objects
            .filter(date_unloading=max_date).exclude(reduce(operator.or_, exclude))
            .values(group[0],group[1])
            .annotate(countData=countData)
            .order_by('-countData')[:5] )           

            nd = ListDataFBone.objects.filter(Q(date_unloading=max_date)).exclude(reduce(operator.or_, exclude)).values("type_error").order_by("type_error").annotate(countData=countData)
        else:
            toppassports = list(ListDataFBone.objects
            .filter(date_unloading=max_date)
            .values(group[0],group[1])
            .annotate(countData=countData)
            .order_by('-countData')[:5] )           

            nd = ListDataFBone.objects.filter(Q(date_unloading=max_date)).values("type_error").order_by("type_error").annotate(countData=countData)
        
        # for x in metodologs.data:
        #     x['connectedPassport']= sorted(list(x['connectedPassport']),key=passport__codeSort,reverse=False)
            
     


        return Response({         
                        # "adress":serializer.data,
                        # "metodologs":  metodologs.data,             
                         "news":news,
                         "toppassports":toppassports,
                         'linear':linear,
                         'totalpassports':totalpassports,
                         'nd':nd
                         }) 

def passport__codeSort(z):    
    x= z['code']
    x=x.replace("_",".")
    x=re.sub(r'[\s_a-zA-Zа-яА-ЯёЁ]',"",str(x))    
    y=x.split(".")
    y=y[0] +"."+ "".join(y[1:]) 
   
    return (float(y))





class Helper(APIView):
    permission_classes = (AllowAny,)
    def get(self,request):
        cont= Contacts.objects.latest('pk')
        serializer = ContactsSerializer(cont,context={"request": request})
        metodologs = PassportMetodologSerializer(SupportPassportMetodolog.objects.all().order_by('methodolog__last_name'), many=True)
        for x in metodologs.data:
            x['connectedPassport']= sorted(list(x['connectedPassport']),key=passport__codeSort,reverse=False)
        return Response({'contacts':serializer.data, 'metodologs':metodologs.data})

    def put(self,request):
       
        data = {"asker":request.user,"question": request.data['question']}
        newob = Questions.objects.create(**data)
        fileattached=[]
        for file in request.FILES.getlist('file'):
            fileattached.append(QuestionFiles(attachmentfile=file, quest=Questions(id=newob.id)))
        QuestionFiles.objects.bulk_create(fileattached)
        return Response(status=200, data={'ок':'ok'})


class Helperacc(View):
    def get(self,request):
        from django.http import JsonResponse
        
        try:
            chob = request.META['HTTP_REFERER'].split("/")
            id = chob[len(chob)-3]
            # print(id)
            Questions.objects.filter(pk = id).update(readed = True, last_reader = request.user, readedtime=datetime.datetime.now())
        
        except Exception:
            pass

        return JsonResponse({'ок':'ok'})

