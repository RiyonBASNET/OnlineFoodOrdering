# Generated by Django 4.0.6 on 2022-09-19 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_auth_tkn_profile_auth_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_verify',
            field=models.BooleanField(default=True),
        ),
    ]
