# Generated by Django 4.1 on 2022-12-13 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panier',
            name='quantite',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]