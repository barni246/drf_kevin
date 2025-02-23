# Generated by Django 5.0.2 on 2025-02-08 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='markets',
            field=models.ManyToManyField(max_length=50, related_name='sellers', to='market_app.market'),
        ),
    ]
