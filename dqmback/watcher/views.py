from django.shortcuts import render
from .models import Watcher
from datetime import date
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
# Create your views here.
class ServiceWatch:
    def __init__(self,request) -> None:       
        # "path": request.path, 
        req = {"user":request.user,'date':date.today(),"razdel":"ЕНС" if "/ens/" in request.path else "ФБ1"}       
        watch,created = Watcher.objects.get_or_create(**req)       
        watch.counted+=1       
        watch.save()

        
class Watchdata(ListAPIView):
    def get(self, request, pk):
       
        data = Watcher.objects.all()
        # serializer = PassportDetailSerializer(passport)
        return Response(data)

    def post(self,request):
        filters=request.data['filters']
       
        if "user__region__isnull" in filters.keys():
       
            # print(".filter(**filters)")
            qfilters = {'user__region__name__in': filters['user__region__name__in']}
            del filters['user__region__isnull']
            del filters['user__region__name__in']
           
            data=Watcher.objects.filter(Q(user__region__name__isnull=True)|Q(**qfilters)).filter(**filters, user__is_staff=False).order_by("date").all().values("user__region__name","user__region__tax_code","date","counted","user__first_name","user__middle_name","user__last_name","razdel")
        # elif 'user__region__name__in' not in filters.keys():

        else:
            data=Watcher.objects.filter(**filters, user__is_staff=False).order_by("date").all().values("user__region__name","user__region__tax_code","date","counted","user__first_name","user__middle_name","user__last_name","razdel")
        return Response(data)