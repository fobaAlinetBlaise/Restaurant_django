# Generated by Django 4.1 on 2022-09-25 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0003_remove_user_role_profil_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profil',
            name='role',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('client', 'client'), ('restaurateur', 'restaurateur')], default='client', max_length=100, null=True),
        ),
    ]
