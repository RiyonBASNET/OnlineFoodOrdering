# Generated by Django 4.0.6 on 2022-09-19 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_is_verify'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_verify',
            field=models.BooleanField(default=False),
        ),
    ]
