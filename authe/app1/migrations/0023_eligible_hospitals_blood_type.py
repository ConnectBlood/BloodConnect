# Generated by Django 5.0 on 2024-03-07 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0022_hospital_details_size_hospital_details_threshold_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eligible_hospitals',
            name='blood_type',
            field=models.CharField(default=None, max_length=358, null=True),
        ),
    ]