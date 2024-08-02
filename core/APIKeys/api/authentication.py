from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from APIKeys.models import ApiKeys


class ApiKeyAuthentication(BaseAuthentication):

    def authenticate(self, request):
        
        #access_key = request.headers.get('X-Access-Key')
        #secret_key = request.headers.get('X-Secret-Key')
        access_key = None
        if 'X-Access-Key' in request.headers:
            access_key = request.headers.get('X-Access-Key')
        
        if 'X-Secret-Key' in request.headers:
            access_key = request.headers.get('X-Access-Key')
        
        if 'X-Access-Key' in request.headers and 'X-Secret-Key' in request.headers:
            access_key = request.headers.get('X-Access-Key')
        
        if not 'X-Access-Key' in request.headers or not 'X-Secret-Key' in request.headers:
            raise AuthenticationFailed('Authentication failed. X-Access-Key and X-Secret-Key headers are required.')
        
        if not access_key == None:

            try:
                key = ApiKeys.objects.get(access_key=access_key)
            except ApiKeys.DoesNotExist:
                raise AuthenticationFailed('Invalid Access Key or Secret Key')
            
            return (key.user,None)
        
        raise AuthenticationFailed('Authentication failed. X-Access-Key and X-Secret-Key headers are required.')

