from django.urls import path,re_path

from .consumers import *

ws_urlpatterns = [
    # re_path(r'ws/task/(?P<task_id>\w+)/$', WSConsumer.as_asgi()),
    re_path(r'ws/loader/', WSLoader.as_asgi()),
    path('ws/informer', WSInformer.as_asgi() ),
    re_path(r'ws/spy/(?P<user>\w+)/$', WSspy.as_asgi())
    # re_path(r'ws/events/(?P<event_id>\w+)/$', WSEventChanger.as_asgi()),
    
]