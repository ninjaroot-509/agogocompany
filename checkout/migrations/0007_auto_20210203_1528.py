# Generated by Django 3.1.3 on 2021-02-03 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_auto_20210203_0151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refund',
            name='order',
        ),
        migrations.RemoveField(
            model_name='order',
            name='ordered',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='Refund',
        ),
    ]
