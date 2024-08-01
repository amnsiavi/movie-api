from rest_framework.serializers import ModelSerializer

from Users.models import UserModel



class UserSerializer(ModelSerializer):

    class Meta:
        
        model = UserModel
        fields = '__all__'

class GETRrequestUserSerializer(ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['id','username','email','is_superuser']