# Generated by Django 4.1 on 2022-10-19 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0006_rename_photo_menu_image_rename_prix_menu_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
