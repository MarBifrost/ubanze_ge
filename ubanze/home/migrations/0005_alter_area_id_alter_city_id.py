# Generated by Django 5.1.4 on 2024-12-19 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_services_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='city',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]