# Generated by Django 5.0.3 on 2024-04-02 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentInstallment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installment_number', models.IntegerField()),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('due_date', models.DateTimeField(auto_now_add=True)),
                ('payment_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]