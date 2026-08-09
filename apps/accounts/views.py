from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer
)

from .services import AuthService


class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        AuthService.register(serializer.validated_data)

        return Response(

            {

                "message": "User Registered Successfully"

            },

            status=status.HTTP_201_CREATED

        )


class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = AuthService.login(serializer.validated_data["user"])

        return Response(data)


class LogoutView(APIView):

    def post(self, request):

        serializer = LogoutSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        AuthService.logout(serializer.validated_data["refresh"])

        return Response(

            {

                "message": "Logout Successful"

            }

        )


class RefreshView(TokenRefreshView):

    pass