# Generated by Django 3.2.11 on 2022-01-11 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20220110_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('ON-SELL', 'ON-SELL'), ('ORDERED', 'ORDERED'), ('BOUGHT', 'BOUGHT')], default='ON-SELL', max_length=15),
        ),
    ]
