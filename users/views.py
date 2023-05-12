from random import choices

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ConfirmCode
from .serializers import UserLoginValidateSerializer, UserCreateValidateSerializer, ConfirmCodeValidateSerializer


class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserLoginValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserCreateValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        activate_code = ''.join(choices('0123456789', k=6))
        user = User.objects.create_user(username=username, password=password, is_active=False)
        code = ConfirmCode.objects.create(user_id=user.id, code=activate_code)
        return Response(status=status.HTTP_201_CREATED,
                        data={'user_id': user.id,
                              'code': code.code})


class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = ConfirmCodeValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            if ConfirmCode.objects.filter(code=request.data['code']):
                User.objects.update(is_active=True)
                return Response(status=status.HTTP_202_ACCEPTED)

            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        except ValueError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
