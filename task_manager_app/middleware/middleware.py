from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token and self.validate_and_set_authorization(request, access_token):
            return None

        if refresh_token:
            access_token = self.refresh_access_token(refresh_token)
            if access_token:
                self.set_authorization(request, access_token)
                request.access_token = access_token
            else:
                self.clear_cookies(request)
                request.COOKIES.pop('refresh_token', None)


    def process_response(self, request, response):
        access_token = getattr(request, 'access_token', None)
        if access_token:
            access_expiry = AccessToken(access_token)['exp'] - timezone.now().timestamp()
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=access_expiry
            )
        return response

    def validate_and_set_authorization(self, request, token):
        try:
            AccessToken(token)
        except TokenError:
            return False
        else:
            self.set_authorization(request, token)
            return True

    def refresh_access_token(self, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
        except TokenError:
            return None
        else:
            return str(refresh.access_token)

    def set_authorization(self, request, token):
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'

    def clear_cookies(self, request):
        request.COOKIES.pop('access_token', None)
        request.COOKIES.pop('refresh_token', None)
