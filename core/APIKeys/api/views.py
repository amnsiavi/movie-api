from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

import uuid
import secrets

from utilities.request_methods.request_methods import GET_REQUEST, POST_REQUEST,DELETE_REQUEST
from utilities.respone_data_formats.data_formats import FETCH_SUCESS, Post_Request_Sucess_MSG
from utilities.error_responses.error_response_messages import Serializer_Invalid_Error_Response, Server_Error_Response, Empty_Object_Error_Response

from Users.permissions import Admin

from APIKeys.models import ApiKeys
from APIKeys.api.serializers import ApiKeySerializer
from Users.models import UserModel

#Request Methods
POST = POST_REQUEST()
GET = GET_REQUEST()


@api_view(GET)
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def generate_keys(request):
    
    try:
        user = request.user
        access_key = uuid.uuid4()
        secret_key = secrets.token_urlsafe()

        data = {
            'user':user.id,
            'access_key': str(access_key),
            'secret_key' : secret_key
        }
        serializer = ApiKeySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'msg':'Keys Generated NOTE!! Dont Share',
                'acces_key':access_key,
                'secret_key':secret_key,
                'status':'success',
            },status=status.HTTP_200_OK)
        else:
            return Response(Serializer_Invalid_Error_Response(serializer), status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(Server_Error_Response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(GET)
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_user_keys(request):

    try:
        user = request.user
        instance = ApiKeys.objects.filter(user=user.id).first()
        if not instance:
            return Response({'msg':'No Keys Associtaed With User', 'status':'False'}, status=status.HTTP_200_OK)
        serializer = ApiKeySerializer(instance)
        return Response(FETCH_SUCESS(serializer,serializer=True),status=status.HTTP_200_OK)
    except Exception as e:
        return Response(Serializer_Invalid_Error_Response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)