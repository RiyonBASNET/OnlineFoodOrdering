# Generated by Django 4.0.6 on 2022-08-24 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0003_fooditems_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditems',
            name='item_image',
            field=models.FileField(null=True, upload_to='static/uploads'),
        ),
    ]
