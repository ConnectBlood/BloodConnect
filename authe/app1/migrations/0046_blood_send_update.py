# Generated by Django 5.0 on 2024-04-08 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0045_message_confirmed_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='blood_send',
            name='update',
            field=models.BooleanField(default=0, null=True),
        ),
    ]
