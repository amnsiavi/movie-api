from django.urls import path

from Movies.api.views import create_movies_list, get_all_movies



urlpatterns = [
    
    
    path('list/create', create_movies_list, name='create_movies_list'),
    path('list/', get_all_movies, name='get_movies'),
    
    
]
