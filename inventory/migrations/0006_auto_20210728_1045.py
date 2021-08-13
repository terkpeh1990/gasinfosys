# Generated by Django 3.1.4 on 2021-07-28 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20210725_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalinventory_records',
            name='approval',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Cancelled', 'Cancelled')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='inventory_records',
            name='approval',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Cancelled', 'Cancelled')], max_length=10, null=True),
        ),
    ]