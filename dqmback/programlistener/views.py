from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponse
from django.views.generic import View
from statistic.models import ListDataFBone
from contacts.models import Questions
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
# from django.views.decorators.csrf import csrf_exempt



import redis
from django.middleware import csrf

def get_or_create_csrf_token(request):
    token = request.META.get('CSRF_COOKIE', None)
    if token is None:
        token = csrf.get_token(request)
        request.META['CSRF_COOKIE'] = token
    request.META['CSRF_COOKIE_USED'] = True
    return request

class LoginView(View):
    
    def get(self,request): 
        request=get_or_create_csrf_token(request)    
        return JsonResponse({'request':request.META['CSRF_COOKIE']}) 
    
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            userinfo= {"id": user.id,
                        "is_superuser": user.is_superuser,
                        "is_staff": user.is_staff,
                        "first_name": user.first_name,
                        'last_name': user.last_name,                        
                        'middle_name': user.middle_name,            
                                        }


            last_upload = ListDataFBone.objects.latest('date_unloading').date_unloading
            waiting_questions= list(Questions.objects.all().order_by("status").values("status").annotate(count= Count("status")))
        

            return JsonResponse({'user': userinfo,
            'upload': last_upload,
            'waiting_questions': waiting_questions
            })  
        else:
            return JsonResponse({"detail": "Введенные имя и пароль не найдены"})    
           



# ---------------------------------------------Функции

    
def thisuser(request):
    theuser = {
                'id': request.user.id,
                'userlogin':request.user,
                'first_name': request.user.first_name,
                'last_name':  request.user.last_name,
                'middlename': request.user.middlename,
                'user_avatar': request.user.user_avatar,
                'otdel':request.user.otdel
    }
    return theuser

