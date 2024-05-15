import jwt
from datetime import datetime, timedelta, UTC

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .modules.common import get_user_from_jwt_token
from .serializers import UserSerializer, CompanySerializer


class SignUpView(APIView):
    def post(self, request):
        if request.data.get('company'):
            company_serializer = CompanySerializer(data=request.data.get('company'))
            company_serializer.is_valid(raise_exception=True)
            company_serializer.save()

            request.data['company'] = company_serializer.data['id']

        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        return Response(user_serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except ObjectDoesNotExist:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'uuid': str(user.uuid),
            'exp': datetime.now(UTC) + timedelta(minutes=30),
            'iat': datetime.now(UTC)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)

        user_seriliazer = UserSerializer(user)

        response.data = {
            'user': user_seriliazer.data,
            'jwt': token
        }
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        user = get_user_from_jwt_token(token)
        serializer = UserSerializer(user)

        response = Response()
        response.data = {
            'user': serializer.data,
            'jwt': token
        }

        return response

    def put(self, request):
        token = request.COOKIES.get('jwt')
        user = get_user_from_jwt_token(token)

        if request.data.get('company'):
            company_serializer = CompanySerializer(data=request.data.get('company'))
            company_serializer.is_valid(raise_exception=True)
            company_serializer.save()

            request.data['company'] = company_serializer.data['uuid']

        serializer = UserSerializer(user, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = Response()
        response.data = {
            'user': serializer.data,
            'jwt': token
        }

        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class CompanyView(APIView):
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        token = request.COOKIES.get('jwt')
        user = get_user_from_jwt_token(token)
        serializer = UserSerializer(user, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = Response()
        response.data = {
            'company': serializer.data['company']
        }

        return response


class ProjectView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        user = get_user_from_jwt_token(token)

        if request.data.get('company'):
            company_serializer = CompanySerializer(data=request.data.get('company'))
            company_serializer.is_valid(raise_exception=True)
            company_serializer.save()

            request.data['company'] = company_serializer.data['uuid']

        serializer = UserSerializer(user, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = Response()
        response.data = {
            'user': serializer.data,
            'jwt': token
        }

        return response