from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions

def enforce_csrf(request):    
    # provides dummy argument to CSRFCheck
    def dummy_get_response(request):
        return None
    check = CSRFCheck(dummy_get_response)
    check.process_request(request)

    reason = check.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied('CSRF Check Failed: %s' % reason)
    
# this class intercepts the request and checks for the presence the JWT token in the cookie and verifies csrf token
class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        # only enforce csrf for unsafe methods
        if request.method not in ['GET', 'HEAD', 'OPTIONS', 'TRACE']:
            enforce_csrf(request)

        return self.get_user(validated_token), validated_token