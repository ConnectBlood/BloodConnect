# Generated by Django 5.0 on 2024-04-08 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0046_blood_send_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blood_send',
            name='update',
        ),
    ]
