from rest_framework.serializers import ModelSerializer

from Movies.models import MoviesModel



class MoviesSerializer(ModelSerializer):
    
    class Meta:
        model = MoviesModel
        fields = '__all__'