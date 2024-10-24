from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        data.update({'user': self.user.username})
        data.update({'first_name': self.user.first_name})
        data.update({'last_name': self.user.last_name})
        data.update({'middle_name': self.user.middle_name})
        data.update({'photo': self.user.photo.url})
        data.update({'lotus': self.user.lotus})
        data.update({'is_superuser': self.user.is_superuser})
        data.update({'region': self.user.region.pk if self.user.region else None})
        
        data.update({'permission': {"pk":self.user.permission.pk, "access":[{"name":x.name, "link":x.link} for x in self.user.permission.permission.all()]}})
       
        return data
        

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('email', 'middle_name', 'last_name', 'first_name', 'username', 'password', 'lotus')