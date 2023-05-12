from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import ConfirmCode


class UserValidateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_password(self, password):
        return password


class UserLoginValidateSerializer(UserValidateSerializer):
    pass


class UserCreateValidateSerializer(UserValidateSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    is_active = serializers.BooleanField(required=False, default=False)

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
            raise ValidationError('User already Exists!')
        except User.DoesNotExist:
            return username


class ConfirmCodeValidateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    code = serializers.CharField(min_length=6, max_length=6)

    def validate_product_id(self, user_id):
        try:
            ConfirmCode.objects.get(id=user_id)
        except ConfirmCode.DoesNotExist:
            raise ValidationError(f'Director with id ({user_id}) not found')
        return
