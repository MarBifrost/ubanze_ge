# Generated by Django 5.1.4 on 2024-12-18 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_is_service_provider_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]