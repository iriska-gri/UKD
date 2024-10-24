from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async,async_to_sync
# from contacts.models import Questions
from statistic.models import ListDataFBone
# from django.db.models import Count

# def createquestion():    
#     layer = get_channel_layer()         
#     waiting_questions= list(Questions.objects.all().order_by("status").values("status").annotate(count= Count("status")))
#     async_to_sync(layer.group_send)(
#     'informer',
#     {
#         'type': 'chat_message',
#         'message': {'waiting_questions': waiting_questions
#     }}
    
#     )

def listfb1_deleted():    
    layer = get_channel_layer()            
    upload= ListDataFBone.objects.latest('date_unloading').date_unloading           
    async_to_sync(layer.group_send)(
    'informer',
    {
        'type': 'chat_message',
        'message': {'upload': upload.strftime("%Y-%m-%d")
    }}
    
    )    


# def question_deleted():    
#     layer = get_channel_layer()  
      
#     waiting_questions= list(Questions.objects.all().order_by("status").values("status").annotate(count= Count("status")))             
#     async_to_sync(layer.group_send)(
#     'informer',
#     {
#         'type': 'chat_message',
#         'message': {'waiting_questions': waiting_questions
#     }}
    
#     )