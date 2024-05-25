import jwt
from datetime import datetime, timedelta, UTC

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import CustomUser, Company, Project, UserStory, Ticket, InvitationUserCompany, InvitationUserCompanyStatus
from .modules.common import get_user_from_jwt_token
from .serializers import UserSerializer, CompanySerializer, ProjectSerializer, UserStorySerializer, TicketSerializer, \
    InvitationUserCompanySerializer


@api_view(['GET'])
def test_message(request):
    return Response({'message': 'Hello, VUE 3!'})


class SignUpView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        user = CustomUser.objects.get(email=request.data.get('email'))

        invitations = InvitationUserCompany.objects.filter(email=user.email, status__code='PEN', user=None)
        invitations.update(user=user)

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
            'exp': datetime.now(UTC) + timedelta(days=7),
            'iat': datetime.now(UTC)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)

        user_serializer = UserSerializer(user)

        response.data = {
            'user': user_serializer.data,
            'jwt': token
        }
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        user = get_user_from_jwt_token(token)
        user_serializer = UserSerializer(user)

        invitations = InvitationUserCompany.objects.filter(user=user, status__code='PEN')
        invitation_serializer = InvitationUserCompanySerializer(invitations, many=True)

        response = Response()
        response.data = {
            'user': user_serializer.data,
            'invitations': invitation_serializer.data,
            'jwt': token
        }

        return response

    def put(self, request, uuid):
        user = CustomUser.objects.get(uuid=uuid)
        serializer = UserSerializer(user, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class InvitationUserCompanyView(APIView):
    def post(self, request):
        user_logged = get_user_from_jwt_token(request.COOKIES.get('jwt'))
        request.data['company'] = user_logged.company

        email = request.data.get('email')

        try:
            user = CustomUser.objects.get(email=email)
            request.data['user'] = user
        except ObjectDoesNotExist:
            pass

        invitations_status = InvitationUserCompanyStatus.objects.get(code='PEN')
        request.data['status'] = invitations_status

        serializer = InvitationUserCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, uuid):
        invitation = InvitationUserCompany.objects.get(uuid=uuid)
        invitation_status = InvitationUserCompanyStatus.objects.get(code=request.data.get('status'))

        if invitation_status and invitation_status.code == 'ACC':
            user = CustomUser.objects.get(uuid=invitation.user.uuid)
            company = Company.objects.get(uuid=invitation.company.uuid)
            user.company.add(company)

        request.data['status'] = invitation_status
        serializer = InvitationUserCompanySerializer(invitation, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class CompanyView(APIView):
    def get(self, request, uuid=None):
        if uuid:
            company = Company.objects.get(uuid=uuid)
            serializer = CompanySerializer(company)
        else:
            companies = Company.objects.all()
            serializer = CompanySerializer(companies, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectView(APIView):
    def get(self, request, uuid=None):
        if uuid:
            project = Project.objects.get(uuid=uuid)
            serializer = ProjectSerializer(project)
        else:
            projects = Project.objects.all()
            serializer = ProjectSerializer(projects, many=True)

        return Response(serializer.data)

    def post(self, request):
        user = get_user_from_jwt_token(request.COOKIES.get('jwt'))

        company_serializer = CompanySerializer(data=request.data.get('company'))
        company_serializer.is_valid(raise_exception=True)
        company_serializer.save()

        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, uuid):
        project = Project.objects.get(uuid=uuid)
        serializer = ProjectSerializer(project, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class UserStoryView(APIView):
    def get(self, request, uuid=None):
        if uuid:
            user_story = UserStory.objects.get(uuid=uuid)
            serializer = UserStorySerializer(user_story)
        else:
            user_stories = UserStory.objects.all()
            serializer = UserStorySerializer(user_stories, many=True)

        return Response(serializer.data)

    def post(self, request):
        user = get_user_from_jwt_token(request.COOKIES.get('jwt'))

        project_serializer = ProjectSerializer(data=request.data.get('project'))
        project_serializer.is_valid(raise_exception=True)
        project_serializer.save()

        serializer = UserStorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, uuid):
        user_story = UserStory.objects.get(uuid=uuid)
        serializer = UserStorySerializer(user_story, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class TicketView(APIView):
    def get(self, request, uuid=None):
        if uuid:
            ticket = Ticket.objects.get(uuid=uuid)
            serializer = TicketSerializer(ticket)
        else:
            tickets = Ticket.objects.all()
            serializer = TicketSerializer(tickets, many=True)

        return Response(serializer.data)

    def post(self, request):
        user = get_user_from_jwt_token(request.COOKIES.get('jwt'))

        project_serializer = ProjectSerializer(data=request.data.get('project'))
        project_serializer.is_valid(raise_exception=True)
        project_serializer.save()

        user_story_serializer = UserStorySerializer(data=request.data.get('user_story'))
        user_story_serializer.is_valid(raise_exception=True)
        user_story_serializer.save()

        serializer = TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, uuid):
        ticket = Ticket.objects.get(uuid=uuid)
        serializer = TicketSerializer(ticket, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, uuid):
        ticket = Ticket.objects.get(uuid=uuid)
        ticket.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)