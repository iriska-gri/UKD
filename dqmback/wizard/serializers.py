from rest_framework import serializers
from .models import *


class WizardListSerializer(serializers.ModelSerializer):
    passport__code = serializers.CharField()
    passport__name = serializers.CharField()
    passport__id = serializers.IntegerField()
    class Meta:
        model = Step
        fields = ('id','passport__code','passport__name','passport__id')
        # depth = 1


class StepWaySerializer(serializers.ModelSerializer):
    stepnow = serializers.ReadOnlyField(source='stepnow.pk')

    class Meta:
        model = StepWay
        fields = ('stepnow','action', 'nextstep')
        depth = 1


class WizardCardSerializer(serializers.ModelSerializer):
    actions = StepWaySerializer(source = 'stepway_set', many=True)
    class Meta:
        model = Step
        # fields =  '__all__'
        fields = ('name','actions', 'passport','textdescription','mode','images','numberstep')
        # exclude = ('passport__code', )
        depth = 1







# class ArticleSerializer(serializers.ModelSerializer):
#     authors = AuthorsOrderSerializer(source='authorsorder_set', many=True)

#     class Meta:
#         model = Article
#         fields = ('title', 'authors')






class WizardSchemaSerializer(serializers.ModelSerializer):
    actions = StepWaySerializer(source = 'stepway_set', many=True)
    class Meta:
        model = Step
        
        # passport__name = serializers.CharField()

        # exclude = ('passport__code', )
        depth = 1
        fields = ('id','numberstep','name', 'actions')
        # fields =  '__all__'


# class PassportStepSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PassportStep
#         fields = '__all__'
#         depth = 1


# class WayPSSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WayPS
#         fields = '__all__'
#         depth = 1

