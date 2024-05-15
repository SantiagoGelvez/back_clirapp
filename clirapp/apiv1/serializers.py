from rest_framework import serializers

from .models import CustomUser, Company, Project, UserStory, Ticket, TicketStatus, TicketComment, InvitationUserCompany


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'uuid', 'name', 'nit', 'email', 'website', 'created_at', 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'uuid', 'first_name', 'last_name', 'email', 'phone', 'company', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        if company := validated_data.get('company'):
            instance.company.add(company)

        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance


class InvitationUserCompanyStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationUserCompany
        fields = ('id', 'code', 'name')


class InvitationUserCompanySerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    status = InvitationUserCompanyStatusSerializer(read_only=True)

    class Meta:
        model = InvitationUserCompany
        fields = ('id', 'uuid', 'company', 'user', 'status', 'email', 'created_at', 'updated_at')


class ProjectSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'uuid', 'name', 'company', 'created_by', 'created_at', 'last_modified')


class UserStorySerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = UserStory
        fields = ('id', 'uuid', 'title', 'project', 'created_by', 'created_at', 'last_modified')


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = ('id', 'code', 'name')


class TicketSerializer(serializers.ModelSerializer):
    user_story = UserStorySerializer(read_only=True)
    status = TicketStatusSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ('id', 'uuid', 'title', 'user_story', 'status', 'created_by', 'created_at', 'last_modified')


class TicketCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    ticket = TicketSerializer(read_only=True)

    class Meta:
        model = TicketComment
        fields = ('id', 'user', 'ticket', 'comment', 'created_at')
