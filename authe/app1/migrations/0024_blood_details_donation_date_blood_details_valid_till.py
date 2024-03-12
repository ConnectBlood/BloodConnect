# Generated by Django 5.0 on 2024-03-08 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0023_eligible_hospitals_blood_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='blood_details',
            name='donation_date',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='blood_details',
            name='valid_till',
            field=models.DateField(blank=True, null=True),
        ),
    ]