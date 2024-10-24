from rest_framework import serializers
from .models import Contacts,SupportPassportMetodolog
from accounts.models import FNSUser
from statistic.models import Passport
from django.core.exceptions import ObjectDoesNotExist

class ContactsSerializer(serializers.ModelSerializer):

    # phone = serializers.CharField(required=False, allow_blank=True, label='Телефон')
    # # topblock = serializers.CharField(required=False, allow_blank=True, label='Верхний блок')
    # # bottomblock = serializers.CharField(required=False, allow_blank=True, label='Нижний блок')
    # imagepath = serializers.ImageField(required=False, label='Изображение')
    class Meta:
        model = Contacts
        fields = '__all__'
    # def get_imagepath(self, car):
    #     request = self.context.get('request')
    #     imagepath_url = car.photo.url
    #     return request.build_absolute_uri(imagepath_url)

# ------------------------------------------------------------------- Информация о методологах для ТП
class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = ('code',)

class FNSUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_full_name')
    def get_full_name(self, obj):
        return f'{obj.last_name} {obj.first_name} {obj.middle_name}'
    class Meta:
        model = FNSUser
        fields = ('name', 'phone')  # in your case since you are using all fields.

class PassportMetodologSerializer(serializers.ModelSerializer):
    methodolog= FNSUserSerializer(required=True)
    connectedPassport = PassportSerializer(read_only=True, many=True)
    
    class Meta:
        model = SupportPassportMetodolog
        fields = '__all__'

    # def create(self, validated_data):
    #     methodolog_name = FNSUserSerializer.create(FNSUserSerializer(), validated_data)
    #     return methodolog_name
# ------------------------------------------------------------------- Информация о методологах для ТП
