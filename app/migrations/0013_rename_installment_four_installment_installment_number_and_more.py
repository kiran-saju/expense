# Generated by Django 5.0.3 on 2024-04-03 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_installment_admin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='installment',
            old_name='installment_four',
            new_name='installment_number',
        ),
        migrations.RemoveField(
            model_name='installment',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='installment',
            name='installment_one',
        ),
        migrations.RemoveField(
            model_name='installment',
            name='installment_three',
        ),
        migrations.RemoveField(
            model_name='installment',
            name='installment_two',
        ),
    ]