# Generated by Django 4.2.13 on 2024-05-14 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_user_spent'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='items',
            name='percentage_discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
