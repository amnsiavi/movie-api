from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer


def Empty_Object_Error_Response():

    return {'errors':'Recieved Empty Object','sucess':False}

def Serializer_Invalid_Error_Response(serializer):

    if not serializer:
        raise ValueError('Serilaizer Object is Required')
    if not isinstance(serializer,Serializer):
        raise TypeError('Argument must be of type Serializer Class')
    return {'errors':serializer.errors,'sucess':False}

def Validation_Error_Response(ve):

    if not ve:
        raise ValueError('ValidationError object is required')
    if not isinstance(ve,ValidationError):
        raise TypeError('Argument must be of type ValidationError((Rest_Framework)) Class')
    return {'errors':ve.detail,'sucess':False}

def Server_Error_Response(e):

    if not e:
        raise ValueError('Exception object is required')
    if not isinstance(e, Exception):
        raise TypeError('Argument must of type Exception Class')
    return {'errors':str(e),'sucess':False}
