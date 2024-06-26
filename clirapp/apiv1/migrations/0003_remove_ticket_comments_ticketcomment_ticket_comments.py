# Generated by Django 5.0.6 on 2024-05-15 17:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiv1', '0002_invitationusercompanystatus_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='comments',
        ),
        migrations.CreateModel(
            name='TicketComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiv1.ticket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='comments',
            field=models.ManyToManyField(related_name='comments', through='apiv1.TicketComment', to=settings.AUTH_USER_MODEL),
        ),
    ]
