# Generated by Django 3.2.11 on 2022-03-04 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_user', '0012_customer_season_country_tb'),
    ]

    operations = [
        migrations.AddField(
            model_name='register_tb',
            name='filter_status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]
