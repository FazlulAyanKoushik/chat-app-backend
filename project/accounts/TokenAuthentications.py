import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from project.settings import SECRET_KEY

from django.contrib.auth import get_user_model
from datetime import timedelta, timezone, datetime

User = get_user_model()


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = self.extract_token(request=request)
        if token is None:
            return None

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            self.verify_token(payload=payload)

            user_id = payload.get("id")
            user = User.objects.get(id=user_id)
            return user

        except (InvalidTokenError, ExpiredSignatureError, User.DoesNotExist):
            raise AuthenticationFailed("Invalid token")

    def verify_token(self, payload):
        if "exp" not in payload:
            raise InvalidTokenError("Token is missing expiration")

        expiration_timestamp = payload["exp"]
        current_timestamp = datetime.now(timezone.utc).timestamp()

        if current_timestamp > expiration_timestamp:
            raise ExpiredSignatureError("Token has expired")

    def extract_token(self, request):
        # auth_header = request.META.get("HTTP_AUTHORIZATION")
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]
        return None

    @staticmethod
    def generate_token(payload):
        expiration = datetime.now(timezone.utc) + timedelta(minutes=60)
        payload["exp"] = expiration.timestamp()
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token

