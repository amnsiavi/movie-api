#Core Imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

#Local Imports
from Users.permissions import Admin, User
from Users.models import UserModel
from Users.api.serializers import UserSerializer,GETRrequestUserSerializer
from utilities.request_methods.request_methods import (
    GET_REQUEST, POST_REQUEST, DELETE_REQUEST, PUT_REQUEST, PATCH_REQUEST,
    DELETE_GET_PUT_PATCH_REQUEST
)
from utilities.respone_data_formats.data_formats import (
    FETCH_SUCESS, Post_Request_Sucess_MSG, 
    Delete_Request_Sucess_MSG,Put_Request_Sucess_MSG, Patch_Request_Sucess_MSG,
    ADMIN_NOT_FOUND, User_NOT_FOUND
    )
from utilities.error_responses.error_response_messages import (
    Empty_Object_Error_Response, Serializer_Invalid_Error_Response, Server_Error_Response, Validation_Error_Response,
)
#REQUEST METHOD 
GET = GET_REQUEST()
POST = POST_REQUEST()
DELETE = DELETE_REQUEST()
PUT = PUT_REQUEST()
PATCH = PATCH_REQUEST()

GET_DELETE_PUT_PATCH = DELETE_GET_PUT_PATCH_REQUEST()


# All Users Views

#Fetch All Users
@api_view(GET)
@permission_classes((IsAuthenticated,Admin))
@authentication_classes([JWTAuthentication])
def get_users(request):
    
    try:
        instance = UserModel.objects.values('id','email','username','is_superuser').all()
        #serializer = UserSerializer(instance, many=True)
        data = FETCH_SUCESS(instance)
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(Server_Error_Response(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#Get Single User
@api_view(GET)
@permission_classes([IsAuthenticated,Admin])
@authentication_classes([JWTAuthentication])
def get_user(request,pk):
    
    try:
        instance = UserModel.objects.values('id','username','email','is_superuser').get(pk=pk)
        return Response(FETCH_SUCESS(instance), status=status.HTTP_200_OK)
    except Exception as e:
        return Response(Server_Error_Response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#Admin Specific Routes


#Fetch Admin Users From DataBase
@api_view(GET)
@permission_classes((IsAuthenticated,Admin))
@authentication_classes([JWTAuthentication])
def get_admins(request):
    
    try:
        instance = UserModel.objects.filter(is_superuser=True)
        serializer = GETRrequestUserSerializer(instance,many=True)
        data = FETCH_SUCESS(serializer,serializer=True)
        return Response(data,status=status.HTTP_200_OK)
    except Exception as e:
        return Response(Server_Error_Response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(POST)
@permission_classes((IsAuthenticated,Admin))
@authentication_classes([JWTAuthentication])
def create_admin(request):
    
    try:
        
        if len(request.data) == 0:
            return Response(Empty_Object_Error_Response(),status=status.HTTP_400_BAD_REQUEST)
        
        if 'username' not in request.data:
            raise ValueError('Username is Required')
        if 'email' not in request.data:
            raise ValueError('Email is Required')
        if 'password' not in request.data:
            raise ValueError('Password is Requried')
        
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user = UserModel.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        if user:
            return Response(Post_Request_Sucess_MSG(),status=status.HTTP_201_CREATED)
        

        
    except ValidationError as ve:
        return Response(Validation_Error_Response(ve),status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(Server_Error_Response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(GET_DELETE_PUT_PATCH)
@permission_classes([IsAuthenticated,Admin])
@authentication_classes([JWTAuthentication])
def get_modify_delete_admin(request,pk):
    
    try:
        if request.method == 'GET':
            instance = UserModel.objects.filter(is_superuser=True,pk=pk).first()
            if not instance:
                return Response({'msg':'Admin Not Found'}, status=status.HTTP_200_OK)
            
            serializer = GETRrequestUserSerializer(instance)
            data = FETCH_SUCESS(serializer,serializer=True)
            return Response(data, status=status.HTTP_200_OK)
        
        elif request.method == 'DELETE':
            instance = UserModel.objects.filter(is_superuser=True,pk=pk)
            if instance:
                instance.delete()
                return Response(Delete_Request_Sucess_MSG(),status=status.HTTP_200_OK)
            else:
                return Response(ADMIN_NOT_FOUND(), status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            if len(request.data) == 0:
                return Response(Empty_Object_Error_Response(),status=status.HTTP_400_BAD_REQUEST)
            
            instance = UserModel.objects.filter(is_superuser=True,pk=pk).first()

            if not instance:
                return Response(ADMIN_NOT_FOUND(),status=status.HTTP_200_OK)
            serializer = UserSerializer(instance,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(Put_Request_Sucess_MSG(),status=status.HTTP_200_OK)
            else:
                return Response(Serializer_Invalid_Error_Response(serializer),status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'PATCH':
            if len(request.data):
                return Response(Empty_Object_Error_Response(),status=status.HTTP_400_BAD_REQUEST)
            instance = UserModel.objects.filter(is_superuser=True,pk=pk).first()
            if not instance:
                return Response(ADMIN_NOT_FOUND(),status=status.HTTP_200_OK)
            serilaizer = UserSerializer(instance,data=request.data,partial=True)
            if serializer.is_vlaid():
                serializer.save()
                return Response(Patch_Request_Sucess_MSG(),status=status.HTTP_200_OK)
            else:
                return Response(Serializer_Invalid_Error_Response(serializer),status=status.HTTP_400_BAD_REQUEST)

    except ValidationError as ve:
        return Response(Validation_Error_Response(ve),status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(Server_Error_Response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

#Regular User Routes

#Get All Regular Users

@api_view(GET)
@permission_classes((IsAuthenticated,User|Admin))
@authentication_classes([JWTAuthentication])
def get_regular_users_all(request):
    
    try:
        instance = UserModel.objects.filter(is_superuser=False).values('id','username','email','is_superuser').all()
        serializer = GETRrequestUserSerializer(instance,many=True)
        data = FETCH_SUCESS(serializer,serializer=True)
        return Response(data,status=status.HTTP_200_OK)
    except Exception as e:
        return Response(Server_Error_Response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Create a Regular User
@api_view(POST)
@permission_classes([IsAuthenticated,Admin])
def create_regular_user(request):
    
    try:
        if len(request.data) == 0:
            return Response(Empty_Object_Error_Response(),status=status.HTTP_400_BAD_REQUEST)
        if 'username' not in request.data:
            raise ValidationError('Username is required')
        if 'email' not in request.data:
            raise ValidationError('Email is required')
        if 'password' not in request.data:
            raise ValidationError('Password is required')
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user = UserModel.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        if user:
            return Response(Post_Request_Sucess_MSG(),status=status.HTTP_201_CREATED)
        
    except ValidationError as ve:
        return Response(Validation_Error_Response(ve),status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(Serializer_Invalid_Error_Response(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Single User GET, DELETE, PUT, PATCH
@api_view(GET_DELETE_PUT_PATCH)
def get_regular_user(request,pk):
    
    try:
        if request.method == 'GET':
            instance = UserModel.objects.filter(is_superuser=False).values('id','username','email').get(pk=pk)
            if not instance:
                return Response(User_NOT_FOUND(),status=status.HTTP_200_OK)
            data = FETCH_SUCESS(instance)
            return Response(data,status=status.HTTP_200_OK)
        
        elif request.method == 'DELETE':
            instance = UserModel.objects.filter(is_superuser=False).first().get(pk=pk)
            if not instance:
                return Response(User_NOT_FOUND(),status=status.HTTP_200_OK)
            instance.delete()
            return Response(Delete_Request_Sucess_MSG(),status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            if len(request.data) == 0:
                return Response(Empty_Object_Error_Response(), status=status.HTTP_400_BAD_REQUEST)
            instance = UserModel.objects.filter(is_superuser=False).first().get(pk=pk)
            if not instance:
                return Response(User_NOT_FOUND(),status=status.HTTP_200_OK)
            serializer = UserSerializer(instance)
            if serializer.is_valid():
                serializer.save()
                return Response(Put_Request_Sucess_MSG(),status=status.HTTP_200_OK)
            else:
                return Response(Serializer_Invalid_Error_Response(serializer),status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'PATCH':
            if len(request.data):
                return Response(Empty_Object_Error_Response(),status=status.HTTP_400_BAD_REQUEST)
            instance = UserModel.objects.filter(is_superuser=False).first().get(pk=pk)
            if not instance:
                return Response(User_NOT_FOUND(),status=status.HTTP_200_OK)
            
            serializer = UserSerializer(instance,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(Patch_Request_Sucess_MSG(),status=status.HTTP_200_OK)
            else:
                return Response(Serializer_Invalid_Error_Response(serializer),status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as ve:
        return Response(Validation_Error_Response(ve),status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(Server_Error_Response(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


