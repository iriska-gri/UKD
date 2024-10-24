from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from accounts.serializers import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('programlistener/', include('programlistener.urls')),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
    path('api/v1/jwt/my_profile/', MyTokenObtainPairView.as_view()),
    path('api/statistic/', include('statistic.urls')),
    path('api/contacts/', include('contacts.urls')),
    
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
