from rest_framework import serializers

from .models import CustomUser, Company, Project, UserStory, Ticket, TicketStatus


class UserSerializer(serializers.ModelSerializer):
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


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'uuid', 'name', 'nit', 'email', 'website', 'created_at', 'updated_at')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'uuid', 'name', 'company', 'created_at', 'updated_at')


class UserStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStory
        fields = ('id', 'uuid', 'name', 'description', 'project', 'created_at', 'updated_at')


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = ('id', 'code', 'name')


class TicketSerializer(serializers.ModelSerializer):
    status = TicketStatusSerializer()

    class Meta:
        model = Ticket
        fields = ('id', 'uuid', 'name', 'status', 'description', 'user_story', 'created_at', 'updated_at')

