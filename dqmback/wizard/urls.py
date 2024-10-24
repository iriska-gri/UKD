from django.urls import path, re_path, include
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
 
    path('list/',views.WizardList.as_view()),

    path('cardread/', views.WizardCard.as_view()),
    path('schemaread/', views.Wizardschema.as_view()),
 

]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)