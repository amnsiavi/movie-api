from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from Movies.models import MoviesModel
from Movies.api.serializers import MoviesSerializer
from Movies.api.pagination import MoviesPagination

from Users.permissions import Admin

from APIKeys.api.authentication import ApiKeyAuthentication

from utilities.request_methods.request_methods import GET_REQUEST, POST_REQUEST
from utilities.error_responses.error_response_messages import Server_Error_Response, Serializer_Invalid_Error_Response, Empty_Object_Error_Response
from utilities.respone_data_formats.data_formats import Post_Request_Sucess_MSG


GET = GET_REQUEST()
POST = POST_REQUEST()


@api_view(POST)
@authentication_classes([ApiKeyAuthentication])
def create_movies_list(request):
    
    try:
        if len(request.data) == 0:
            print("Empty object Bad Response")
            return Response(Empty_Object_Error_Response(), status=status.HTTP_400_BAD_REQUEST)
        serializer = MoviesSerializer(data=request.data)
        if serializer.is_valid():
            print('Serializer is Valid')
            serializer.save()
            return Response(Post_Request_Sucess_MSG(),status=status.HTTP_201_CREATED)
        else:
            print('Serializer in InValid Response')
            return Response(Serializer_Invalid_Error_Response(serializer), status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response(Server_Error_Response(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(GET)
@authentication_classes([ApiKeyAuthentication])
def get_all_movies(request):
    
    try:
        paginator = MoviesPagination()
        instance = MoviesModel.objects.all()
        if 'title' in request.query_params:
            title = request.query_params.get('title')
            instance = instance.filter(title=title)
        instance_paginated = paginator.paginate_queryset(instance,request)
        serializer = MoviesSerializer(instance_paginated, many=True)
        #return Response({'data':serializer.data}, status=status.HTTP_200_OK)
        return paginator.get_paginated_response({
            'data':serializer.data,
            'status': status.HTTP_200_OK
        })
    except Exception as e:
        return Response(Server_Error_Response(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)