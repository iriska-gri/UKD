from django.urls import path
from . import views

urlpatterns = [   
    path('auth/', views.LoginView.as_view()),

]