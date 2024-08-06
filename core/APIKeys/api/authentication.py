from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from APIKeys.models import ApiKeys


class ApiKeyAuthentication(BaseAuthentication):

    def authenticate(self, request):
        
        #access_key = request.headers.get('X-Access-Key')
        #secret_key = request.headers.get('X-Secret-Key')
        valid_access_key = 'X-Access-Key'
        access_key = None
        
        if valid_access_key in request.headers:
            access_key = request.headers.get(valid_access_key)
        
        
        if not access_key == None:

            try:
                key = ApiKeys.objects.get(access_key=access_key)
            except ApiKeys.DoesNotExist:
                raise AuthenticationFailed('Invalid Access Key or Secret Key')
            
            return (key.user,None)
        
        raise AuthenticationFailed('Authentication failed. X-Access-Key are required.')

