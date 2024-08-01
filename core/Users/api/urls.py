from django.urls import path

from Users.api.views import get_users,get_user, get_admins, create_admin, get_modify_delete_admin, get_regular_users_all, create_regular_user, get_regular_user



urlpatterns = [
    #Routes For all Users

    path('list/',get_users,name='get_users'),
    path('<int:pk>/',get_user,name='get_user'),
    # End Of Url Patterns

    #Routes For Admin User
    path('admin/list',get_admins,name='get_admins'),
    path('admin/create',create_admin,name='create_admin'),
    path('admin/<int:pk>',get_modify_delete_admin,name='get_modify_delete_admin'),
    #End of Url Patterns


    #Regualar User Routes
    path('regular/list',get_regular_users_all,name='get_all_regular_users'),
    path('regular/create',create_regular_user,name='create_regular_user'),
    path('regular/<int:pk>',get_regular_user,name='get_user'),


]
