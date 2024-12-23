# Generated by Django 5.0.2 on 2024-12-23 17:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('supplier', '0002_alter_supplier_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='suppliers', to='account.account'),
            preserve_default=False,
        ),
    ]
