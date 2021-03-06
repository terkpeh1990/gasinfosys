# Generated by Django 3.1.4 on 2021-02-02 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='helpdesk.district'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='helpdesk.region'),
        ),
    ]
