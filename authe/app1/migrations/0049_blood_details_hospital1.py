# Generated by Django 5.0 on 2024-04-08 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0048_request_list_available_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='blood_details',
            name='hospital1',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
    ]
