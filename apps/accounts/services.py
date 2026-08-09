from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class AuthService:

    @staticmethod
    def register(validated_data):

        return User.objects.create_user(

            username=validated_data["username"],

            email=validated_data["email"],

            full_name=validated_data["full_name"],

            password=validated_data["password"]

        )

    @staticmethod
    def login(user):

        refresh = RefreshToken.for_user(user)

        return {

            "access": str(refresh.access_token),

            "refresh": str(refresh),

            "user": {

                "id": user.id,

                "full_name": user.full_name,

                "email": user.email

            }

        }

    @staticmethod
    def logout(refresh_token):

        token = RefreshToken(refresh_token)

        token.blacklist()