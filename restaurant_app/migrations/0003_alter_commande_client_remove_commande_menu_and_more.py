# Generated by Django 4.1 on 2022-12-13 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0002_alter_panier_quantite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='commande',
            name='menu',
        ),
        migrations.AddField(
            model_name='commande',
            name='menu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_com', to='restaurant_app.menu'),
        ),
    ]
