from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:

        model = User

        fields = [

            "full_name",
            "username",
            "email",
            "password"

        ]

    def create(self, validated_data):

        password = validated_data.pop("password")

        user = User(**validated_data)

        user.set_password(password)

        user.save()

        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField()

    def validate(self, attrs):

        user = authenticate(

            username=attrs["email"],
            password=attrs["password"]

        )

        if not user:

            raise serializers.ValidationError("Invalid Credentials")

        attrs["user"] = user

        return attrs


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()