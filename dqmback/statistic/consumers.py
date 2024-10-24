from venv import create
from xml.etree.ElementTree import tostring
from django.dispatch.dispatcher import receiver
import redis
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
# from .my_mixin import HelpMixin,  ProjectActions, update_task_status_listeners, update_event_status_listeners
import datetime
import numpy as np
from dqmback.settings import MEDIA_ROOT
from .models import *
from ens.models import ListDataFBone as ENSlist
from ens.models import Passport as ENSpassport
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
import csv
from django.contrib.auth import get_user_model
import datetime as DT
import json
import os
from django.db.models import Count
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q, F,CharField, Value
import pandas as pd
from .serializers import ListDataFBoneSerializer, JustifyDataFBoneSerializer, PassportDetailSerializer, PassportSerializer
from accounts.models import FNSUser
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async,async_to_sync
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from contacts.models import Questions
import channels
from urllib.parse import parse_qs
def log_error(func):
    from functools import wraps
    import traceback

    @wraps(func)
    def wrapper(*arg, **kwargs):
        try:
            return func(*arg, **kwargs)
        except Exception as exc:
            
            raise
    return wrapper

class WSLoader(WebsocketConsumer):
    def connect(self):
        # client = redis.Redis(host='127.0.0.1')
        self.room_name = "Loader"
        # self.client=client
        self.room_group_name = f"group{self.room_name}"
        self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        

        self.accept()
        userid = self.scope['user'].id
        self.send(text_data=json.dumps({"opening":1}))
      

    def receive(self, text_data):
        
        text_data_json = json.loads(text_data)        
        
        getattr(self, text_data_json['attr'])(text_data_json['filepath'])
     
   

    def correct_foreing(self, model, arg):
        try:
            req = model.objects.get(**arg)
        except ObjectDoesNotExist:
            model.objects.create(**arg)
            req = model.objects.get(**arg)
        return req

    def regions(self, file):
        df = pd.read_excel(file, dtype=str)
        for row in df.values:
            tax = row[0].rjust(2, '0')
            Region.objects.update_or_create(tax_code=tax, defaults={'tax_code': tax, 'name': row[1]})
    
    def passports(self, file):
        # print("ssssssssssssssssssssssssssssssssssss!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        df = pd.read_excel(file, dtype=str)
        for row in df.values:
            Passport.objects.update_or_create(code=row[1], defaults={'code': row[1], 'name': row[2]})
    # !Внимательный тест
    def inn(self,inn):
        if len(inn) in [9,11]:
            return '0'+ inn
        else:
            return inn
    def inclu(self,input):
        includes = {'32_105': '32_105', '5_ЮЛ': '5 ЮЛ', '5_ИП': '5 ИП'}
        return  includes[input] if input in includes.keys()  else input.replace('_', '.')
    
    
    def FB1(self, file):
        
        self.send(text_data=json.dumps({"opening":1}))
        file=os.path.join(MEDIA_ROOT, file)
        t=datetime.datetime.now()
        xl = pd.ExcelFile(file)
        pastable=Passport
        listdata= ListDataFBone
        if xl.sheet_names[0]=='ФБ1':
            typeload='fb1'
            pastable=Passport
            listdata= ListDataFBone
        elif xl.sheet_names[0]=='ЕНС':
            typeload='ens'
            pastable=ENSpassport
            listdata= ENSlist
            

        totalold=listdata.objects.all().count()    
        
        df = pd.read_excel(file, dtype=str, sheet_name=0)
        
       
        self.send(text_data=json.dumps({"columnwork":1}))
        df["Дата выгрузки"]= df["Дата выгрузки"].fillna("1900-01-01")
        if df['ID_ошибки'].isnull().sum():
            self.send(text_data=json.dumps({"error": "У вас в файле в столбце ID_ошибки пустые значения. Не буду загружать",
                                                    "completedshow":1 
                                                                             }))
            return

        df = df.fillna('')
        
        data_insert=[]


        df["Дата выгрузки"] = df["Дата выгрузки"].str.split().str[0]
        df["Паспорт"] = df["Паспорт"].apply(self.inclu)
        
        totalrows=df.shape[0]
        self.send(text_data=json.dumps({"totalrows":totalrows}))
        regions,passport={},{}
        indx=1
        justif=0 
        df.to_csv(f"{file[:-4]}2.csv",';',index=False,quoting= csv.QUOTE_ALL, quotechar='"',header=False)
        t2=datetime.datetime.now()
        for chunk in pd.read_csv(f"{file[:-4]}2.csv", sep=';', header=None, na_values='NULL',keep_default_na=False, dtype=str,chunksize=10000, engine='python'):
            for row in chunk.values:     
                if (datetime.datetime.now()-t2).total_seconds()>1 or indx in [1,totalrows]:     
                    self.send(text_data=json.dumps({"rowwork":indx}))
                    t2=datetime.datetime.now()
                if row[0] != '':            
                    
                    try:
                        if row[0] not in regions.keys():
                            regions[row[0]]=Region.objects.get(tax_code=row[0])
                        if row[1] not in passport.keys():
                            passport[row[1]]= pastable.objects.get(code=row[1])                  

                        if typeload=='fb1' and len(list(Justify.objects.filter(fix_status=True, agreement_date__lt=row[8],listdate__id_error=row[7])))>0:
                            justif+=1 
                            indx+=1
                            self.send(text_data=json.dumps({"justific":justif}))
                            continue    
                        arg = {
                            'region': regions[row[0]],
                            'passport': passport[row[1]],
                            'date_unloading': row[8],
                            'fid': str(row[4]).replace(".0",''),
                            'inn': self.inn(str(row[5]).replace(".0",'')),
                            'ogrn': row[6],
                            'id_error': row[7],
                            'type_error': row[9] if row[8] else None,
                            'nocode':row[2],
                            'rocode':row[3]

                        }
                        data_insert.append(listdata(**arg))
                        indx+=1
                        
                    except Exception as e:
                        print("Ошибочка")
                        totalnew=listdata.objects.all().count()
                        self.send(text_data=json.dumps({"error": f"в строке {indx+1}: {', '.join(str(r) for r in row)} - {e}",
                                                        "completed":totalnew-totalold,
                                                        "completedshow":1 
                                                                                }))
                        return
            
            # self.send(text_data=json.dumps({"basewrighting":True}))
            listdata.objects.bulk_create(data_insert, ignore_conflicts=True)
            data_insert=[]
     
        
        try:           
            totalnew=listdata.objects.all().count()
            post_save.send(sender = listdata, instance=0, created=True)
        except Exception as e:
            totalnew=listdata.objects.all().count()
            self.send(text_data=json.dumps({"error": f"записи: {e}",
                                                    "completedshow":1,
                                                    "completed":totalnew-totalold, 
                                                                             }))
            return 

        self.send(text_data=json.dumps({"completed":totalnew-totalold,
                                        "completedshow":1                           }))
        
        
    

    

    
    
    def passport(self, file):

        df = pd.read_excel(file, dtype=str)
        df = df.fillna('')

        values = iter(df.values)
        next(values)
 
        for row in values:
      
            try:

                passport = Passport.objects.get(code=row[1])
                
                if (row[4] != ''):
                    passport.mode = True if int(row[4]) == 1 else False
                if (row[3] != ''):
                    passport.date_of_including_of_the_initial_list = row[3].split()[0]
           
                passport.save()

            except:
                pass
      
class WSInformer(AsyncWebsocketConsumer):
 

    async def connect(self):
        client = redis.Redis(host='127.0.0.1')
        
        self.client=client

        self.room_group_name = "informer"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        # userid = self.scope['user'].id
        
        
        # r = redis.Redis.from_url(REDIS_URL_USED_BY_CHANNELS_2)
      
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {'message':'connected'}
            })
        layer = get_channel_layer()   
       
      
       

    async def chat_message(self, event, type='chat_message'):
        
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
        
        
   
        
        
        

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
      
      
      
        await self.channel_layer.group_send(
            self.room_group_name,
            {
            'type': 'chat_message',
            'message': text_data
            }
        )
    # @staticmethod
def zmanipilate(x):
    z = json.loads(x[0])
    z["outed"] = int(round(x[1]))
    return z

class WSspy(AsyncWebsocketConsumer):
    
        
    async def connect(self):
        client = redis.Redis(host='127.0.0.1')
        
        self.client=client
        # self.room_name = "Spyman"
        # print(self.scope['user'].is_anonymous)

        arr = self.scope['path'].split("/")
       
        timenow = int(round(datetime.datetime.now().timestamp()))
        self.scope["usertime"] = timenow 
        if arr[len(arr)-2]!="watcher":

            key=arr[len(arr)-2]
                       
            ip = parse_qs(self.scope["query_string"].decode("utf8"))["ip"][0]
            if key=="logged":
                region = parse_qs(self.scope["query_string"].decode("utf8"))["region"][0]
             
                sn = parse_qs(self.scope["query_string"].decode("utf8"))["sn"][0]
                client.rpush(key, json.dumps({"ip":ip,"entered":timenow,"region":str(region),"sn":sn}))
            else:
                client.rpush(key, json.dumps({"ip":ip,"entered":timenow}))
            client.zremrangebyscore(f'{key}_outed',0,int(timenow-86400))  
            
                

       
        info={
             'anonymousnow' : [json.loads(x) for x in client.lrange('anonymous', 0, -1)],
            'loggednow' : [json.loads(x) for x in client.lrange('logged', 0, -1)],
            'anonymous_outed' :  [zmanipilate(x) for x in client.zrange('anonymous_outed', 0, -1, withscores=True)],
            'logged_outed' :  [zmanipilate(x) for x in client.zrange('logged_outed', 0, -1, withscores=True)],           
            
        }        
       
        
       
       
        self.room_group_name = "Spyman"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()     
       
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {'action':'updateinfouser','data':info}
            })
        layer = get_channel_layer()   
       
    async def chat_message(self, event, type='chat_message'):
       
        message = event['message']        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))    
     
        
    async def receive(self, text_data):
        
      
        await self.channel_layer.group_send(
            self.room_group_name,
            {
            'type': 'chat_message',
            'message': text_data
            }
        )        

 
    
    
    async def disconnect(self, close_code):
        client = redis.Redis(host='127.0.0.1')        
        self.client=client
        # arr = self.scope['path'].split("/")
        # key =arr[len(arr)-2]
        timenow = int(round(datetime.datetime.now().timestamp()))
       
        

        for key in ['anonymous', 'logged']:
            i=0
            client.zremrangebyscore(f'{key}_outed',0,timenow-604800)
            
            while i<client.llen(key):                
                ob = json.loads(client.lindex(key, i))
                            
                if ob['entered']==self.scope["usertime"]:
                    
                    # zadd записывает, когда и кто зашел на сайт и когда зашел (zadd очки)
                    client.zadd(f'{key}_outed', {client.lindex(key, i) : timenow})
                    # удаляем пользователя из активных. длина - это сколько на сайте пользователей. содержание - кто
                    client.lrem(key, i, client.lindex(key, i))
                if ob['entered']<timenow-86400:
                    client.lrem(key, i, client.lindex(key, i))                
                i+=1                  
                    
               
               
               
          
        info={
             'anonymousnow' : [json.loads(x) for x in client.lrange('anonymous', 0, -1)],
            'loggednow' : [json.loads(x) for x in client.lrange('logged', 0, -1)],
            'anonymous_outed' :  [zmanipilate(x) for x in client.zrange('anonymous_outed', 0, -1, withscores=True)],
            'logged_outed' :  [zmanipilate(x) for x in client.zrange('logged_outed', 0, -1, withscores=True)],           
            
        }      
        await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'chat_message',
            'message': {'action':'updateinfouser','data':info}
        })
     
   