# Generated by Django 5.0 on 2024-03-28 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0036_eligible_hospitals_requested_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='eligible_hospitals',
            name='total_wt',
            field=models.FloatField(default=None, null=True),
        ),
    ]
