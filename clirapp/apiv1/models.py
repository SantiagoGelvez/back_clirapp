import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class Company(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    nit = models.CharField(max_length=15)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    @staticmethod
    def create(**kwargs):
        try:
            company = Company.objects.create(**kwargs)
            return company
        except Exception as e:
            raise e


class CustomUser(AbstractUser):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.CharField(max_length=15, null=True, blank=True)
    company = models.ManyToManyField(Company, related_name='users', blank=True)
    username = None

    def __str__(self):
        return f'{self.username}'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class AbstractStatus(models.Model):
    code = models.CharField(max_length=3, primary_key=True, unique=True)
    name = models.CharField(max_length=20)

    class Meta:
        abstract = True


class InvitationUserCompanyStatus(AbstractStatus):
    def __str__(self):
        return f'{self.code} - {self.name}'


class InvitationUserCompany(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey(InvitationUserCompanyStatus, on_delete=models.CASCADE, to_field='code', null=True, blank=True)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.email} - {self.company.name}'


class Project(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserStory(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TicketStatus(AbstractStatus):
    def __str__(self):
        return f'{self.code} - {self.name}'


class Ticket(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    comments = models.ManyToManyField(CustomUser, related_name='comments', through='TicketComment', through_fields=('ticket', 'user'))
    status = models.ForeignKey(TicketStatus, on_delete=models.CASCADE, to_field='code')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    assigned_to = models.ManyToManyField(CustomUser, related_name='tickets', through='TicketAssignedTo', through_fields=('ticket', 'user'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ticket.title} - {self.user.email}'


class TicketAssignedTo(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ticket.title} - {self.user.email}'
