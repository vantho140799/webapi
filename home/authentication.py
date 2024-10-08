import base64
import os
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from cryptography.fernet import Fernet

key = base64.urlsafe_b64encode(os.urandom(32))
cipher = Fernet(key)

class ExpiringTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        encrypted_token = request.META.get('HTTP_AUTHORIZATION')
        if encrypted_token:
            try:
                token = cipher.decrypt(encrypted_token.encode()).decode()  # Giải mã token
                user = self.get_user(token)  # Tìm người dùng từ token
                return (user, None)  # Không cần trả về token
            except Exception:
                raise AuthenticationFailed('Invalid token.')
        return None

    def get_user(self, token):
        try:
            user = User.objects.get(username=token)
            return user
        except User.DoesNotExist:
            return None
