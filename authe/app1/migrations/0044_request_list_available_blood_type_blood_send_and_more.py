# Generated by Django 5.0 on 2024-04-07 11:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0043_eligible_hospitals_is_accepted_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='request_list',
            name='available_blood_type',
            field=models.CharField(default=None, max_length=546, null=True),
        ),
        migrations.CreateModel(
            name='blood_send',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donating_hospital', models.CharField(max_length=354)),
                ('available_blood_type', models.CharField(default=None, max_length=546, null=True)),
                ('amount', models.IntegerField()),
                ('requesting_hospital', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='message_confirmed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donating_hospital', models.CharField(max_length=354)),
                ('available_blood_type', models.CharField(default=None, max_length=546, null=True)),
                ('amount', models.IntegerField()),
                ('requesting_hospital', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
