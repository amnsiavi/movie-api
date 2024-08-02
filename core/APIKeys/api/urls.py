from django.urls import path

from APIKeys.api.views import generate_keys, get_user_keys



urlpatterns = [
    
    path('generate-key/', generate_keys, name='generate_key'),
    path('get-keys/', get_user_keys, name='get_user_keys'),
    

]