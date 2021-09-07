import uuid

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from . import models
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def validate_password(self, value: str) -> str:
        return make_password(value)

    class Meta:
        model = User
        exclude = (
            'password',
            'is_active',
        )


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'email_code'
        )

    def create(self, fields):
        fields['username'] = fields['email']
        fields['email_code'] = uuid.uuid4()
        fields['password'] = fields['email_code']
        user = User.objects.create_user(**fields)
        send_mail(
            'Your confirmation code from YAMDB API',
            f'Hello. Your API code: {fields["email_code"]}',
            "foryandextest@mail.ru",  # from e-mail
            ["foryandextest@mail.ru"],  # change to [{fields['email']}]
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    email_code = serializers.CharField()

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        email_code_user = models.User.objects.all().get(
            email=attrs['email']
        ).email_code
        if attrs['email_code'] == email_code_user:
            user = authenticate(
                username=attrs['email'],
                password=attrs['email_code']
            )
        else:
            return 'Incorrect email_code'

        refresh = self.get_token(user)

        data = {}

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
