from rest_framework.serializers import ModelSerializer

from APIKeys.models import ApiKeys

class ApiKeySerializer(ModelSerializer):

    class Meta:
        model = ApiKeys
        
        fields = ['id','user','access_key','secret_key','created_at']

        read_only_fields = ['secret_key','created_at']
