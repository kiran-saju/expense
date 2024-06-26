# Generated by Django 5.0.3 on 2024-04-09 03:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_rowmaterials'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('due_date', models.DateTimeField(auto_now_add=True)),
                ('paid_date', models.DateTimeField(auto_now=True)),
                ('paid_status', models.BooleanField(default=False)),
                ('row_materials', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.rowmaterials')),
                ('staff_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.staff')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.supplier')),
            ],
        ),
    ]
