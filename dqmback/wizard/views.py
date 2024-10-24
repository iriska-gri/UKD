
from urllib import request
from django.shortcuts import render
from statistic.models import Passport
from .models import *
from .serializers import *
from rest_framework import generics, viewsets
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView
import json
from statistic.views import customordering


class WizardList(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = WizardListSerializer
    def get_queryset(self):
        nowsort =self.request.query_params.get('sort')
        filters={}
        try:
            filters =json.loads(self.request.query_params.get('filters'))
        except TypeError:
            filters={}
        
        return customordering(Step.objects.filter(numberstep = 1).filter(**filters).distinct(nowsort.replace("-","")).order_by(nowsort).values('id','passport__id','passport__code','passport__name'),nowsort)


class WizardCard(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = WizardCardSerializer
  

    def get_queryset(self):
        stepid={}       
        stepid =json.loads(self.request.query_params.get('param'))        
        return  Step.objects.filter(**stepid)


class Wizardschema(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = WizardSchemaSerializer


    def get_queryset(self):        
        stepid={}       
        stepid =json.loads(self.request.query_params.get('param'))   
        
        return  Step.objects.filter(**stepid).filter(numberstep__isnull=False).order_by('numberstep')
        
        