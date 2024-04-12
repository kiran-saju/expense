# Generated by Django 5.0.3 on 2024-04-03 05:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_installment_alter_bill_installment_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='installment',
            name='admin',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
