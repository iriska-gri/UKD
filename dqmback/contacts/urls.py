from django.urls import path
from . import views

urlpatterns = [
    path('ipgetter/',views.Ipgetter.as_view()),
    path('helper/', views.Helper.as_view()),
    path('helperacc/', views.Helperacc.as_view()),
    path('mainpage/', views.Mainpage.as_view()),
]