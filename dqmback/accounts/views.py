from django.contrib.auth.models import Group
from .models import *
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import AllowAny
# from .serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import random
import string
import requests, os
# from time import timedelta

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = FNSUser.objects.all().order_by('-date_joined')
    # serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    # serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class Logout(APIView):
    def get(self, request, format=None): 
         
        # request.user.auth_token.delete()        
        return Response(status=status.HTTP_200_OK)

class Restore(APIView):
    permission_classes = [AllowAny]
    def get(self,request,restore):
        # print(restore)

        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        # print(request.data)
       
        if 'lotus' in request.data.keys():       
            try:
                lotus = request.data['lotus']
                user = FNSUser.objects.filter(lotus=lotus)[0]              
                
                randomurl = generate_random_string(50)
                up, created = Restoretable.objects.update_or_create(
                        user=user, defaults={"randomurl": randomurl}
                )
              
                data = {'sendto':[user.lotus], 'subject':f'Восстановление пароля Веб-Сервиса УКД','body_text': f'В форме на сайте введите проверочный код: {randomurl}' }
                resp =requests.post('http://10.252.44.13:8005/', data=data ,files=[])  
                return Response(status=status.HTTP_200_OK, data={'user':{'login':user.username,"first_name": user.first_name,"last_name":user.last_name,"middle_name":user.middle_name}})
            except Exception as e:
                return Response(status=status.HTTP_200_OK , data={'error': "Произошла ошибка. Попробуйте позднее"})
        elif 'randomurl' in request.data.keys():

            try:
                restor = Restoretable.objects.get(randomurl =  request.data['randomurl'])                
                user = FNSUser.objects.get(pk= restor.user.pk)               
                user.set_password(request.data['password'])
                user.save()
                restor.delete()
                return Response(status=status.HTTP_200_OK , data={'message': "Пароль успешно сброшен"})
            except Exception as e:
                return Response(status=status.HTTP_200_OK , data={'error': "Произошла ошибка. Попробуйте позднее"})



def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string