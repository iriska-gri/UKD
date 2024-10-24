from pkg_resources import require
from rest_framework import serializers

from accounts.models import FNSUser
from .models import *
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 150
    page_size_query_param = 'page_size'
    max_page_size = 1500


class ListDataFBoneSerializer(serializers.ModelSerializer):

    region__name = serializers.CharField()
    region__tax_code = serializers.CharField()
    passport__code = serializers.CharField()
    passport__name = serializers.CharField()
    class Meta:
        model = ListDataFBone
        fields = ('date_unloading', 'region__name', 'region__tax_code', 'passport__code', 'inn', 'ogrn', 'fid', 'id_error','nocode','rocode','passport__name')
        





class PassportDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passport
        fields = "__all__"


class SubsisS(serializers.ModelSerializer):
    class Meta:
        model = SubSystem
        fields = ('name',)


class PassportSerializer(serializers.ModelSerializer):

    code = serializers.CharField(required=True, allow_blank=False, label='Код паспорта')
    name = serializers.CharField(required=False, allow_blank=True, label='Имя паспорта')

    responsible = serializers.CharField(source='description_data.responsible.name', required=False, allow_blank=True, label='Ответственный')
    sub_system = SubsisS(source='description_data.sub_system', read_only=True,  many=True,  label='Подсистема')
    
    criticality = serializers.CharField(source='description_data.criticality.name', required=False, allow_blank=True, label='Критичность')
    priority = serializers.CharField(source='description_data.priority.name', required=False, allow_blank=True, label='Приоритет')
    reason_occurrence = serializers.CharField(source='description_data.reason_occurrence', required=False, allow_blank=True, label='Причина возникновения')
    detection_method = serializers.CharField(source='description_data.detection_method', required=False, allow_blank=True, label='Способ выявления')
    probability_of_occurrence = serializers.BooleanField(source='description_data.probability_of_occurrence', required=False, allow_null=True,  label='Вероятность возникновения')

    algorithm_creation_period = serializers.DateField(source='description_data.algorithm_creation_period', required=False, allow_null=True, label='Срок создания алгоритма')
    selection_aproval_period = serializers.DateField(source='description_data.selection_aproval_period', required=False, allow_null=True, label='Срок согласования отбора')
    date_of_formation_of_the_initial_list = serializers.DateField(source='description_data.date_of_formation_of_the_initial_list', required=False, allow_null=True, label='Дата формирования первоначального перечня')
    count_into_the_initial_list = serializers.CharField(source='description_data.count_into_the_initial_list', required=False, allow_blank=True, allow_null=True, label='Количество в первоначальном перечне')

    description_algorithm = serializers.CharField(source='description_data.description_algorithm', required=False, allow_blank=True, label='Описание алгоритма')
    external_sources = serializers.CharField(source='description_data.external_sources', required=False, allow_blank=True, label='Необходимость получения дополнительных сведений из внешних источников')

    reason_occurrence_new = serializers.CharField(source='description_data.reason_occurrence_new', required=False, allow_blank=True, label='Причина возникновения новых')
    measures_to_eliminate_causes = serializers.CharField(source='description_data.measures_to_eliminate_causes', required=False ,allow_blank=True, label='Меры по исключению причин возникновения')
    application_numbers = serializers.CharField(source='description_data.application_numbers', required=False, allow_blank=True, label='Номера заявок в СУТ')

    class Meta:
        model = Passport
        fields = ('code','name', 'description', 'code_name_process', 'date_of_including_of_the_initial_list', 'mode', 'responsible', 'sub_system', 'criticality', 'priority', 'reason_occurrence', 'detection_method', 'probability_of_occurrence', 'algorithm_creation_period', 'selection_aproval_period', 'date_of_formation_of_the_initial_list', 'count_into_the_initial_list', 'description_algorithm','external_sources', 'reason_occurrence_new', 'measures_to_eliminate_causes', 'application_numbers')
        
    # def validate(self, data):
    #     # sub_system = data['sub_system']  # access M2M key
    #     # my code
    #     print (data)
    #     return data



    def create(self, validated_data):
       
        if self.method == "add":
            try:
                passport = Passport.objects.get(code=validated_data['code'])
                raise Exception('Паспорт с таким именем уже существует')
            except ObjectDoesNotExist:
                Passport.objects.create(code=validated_data['code'])

        passport = Passport.objects.get(code=validated_data['code'])
        
        
        
        if 'description_data' in validated_data: 
                       
            for (field, model) in {'responsible': ResponsibleMonitoring, 'sub_system': SubSystem, 'criticality': Criticality, 'priority': Priority}.items():
                
                if field in validated_data['description_data']:

                    name = validated_data['description_data'][field]['name']
                    obj = None
                    try:
                        obj = model.objects.get(name=name)
                        
                        
                    except ObjectDoesNotExist:
                        if name != '':
                            model.objects.create(name=name)
                            obj = model.objects.get(name=name)
                            
                        else:
                            del validated_data['description_data'][field]
                    
                    if obj:
                        validated_data['description_data'][field] = obj
            
            if passport.description_data:
                
                for (key, val) in validated_data['description_data'].items():
                    setattr(passport.description_data, key, val)
                    
                passport.description_data.save()
                # passport.description_data.sub_system.clear()
                # добавить надо м2м
                description_data=passport.description_data
                del validated_data['description_data']
            else:
                
                description_data = DescriptionData(**validated_data['description_data'])
                description_data.save()
                validated_data['description_data'] = description_data

            arr =[x for x in self.datasbs]          
            
            if passport.description_data and passport.description_data.sub_system:
                for x in passport.description_data.sub_system.all():
                    if x not in arr:                    
                        passport.description_data.sub_system.remove(SubSystem.objects.get(name=x))
            if len(arr)>0:
                
                for x in arr:
                            description_data.sub_system.add(SubSystem.objects.get(name=x))

                 
        return Passport.objects.filter(code=validated_data['code']).update(**validated_data)



# class DinamicSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Dynamics
#         fields = '__all__'

