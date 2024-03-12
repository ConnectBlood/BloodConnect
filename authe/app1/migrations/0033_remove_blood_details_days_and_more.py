# Generated by Django 5.0 on 2024-03-08 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0032_remove_blood_details_donation_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blood_details',
            name='days',
        ),
        migrations.AddField(
            model_name='blood_details',
            name='donation_date',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='blood_details',
            name='valid_days',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blood_details',
            name='valid_till',
            field=models.DateField(blank=True, null=True),
        ),
    ]