# Generated by Django 5.0 on 2024-02-20 12:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_remove_hospital_details_org_phone_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='bloodrequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]