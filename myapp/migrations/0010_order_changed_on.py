# Generated by Django 2.1.1 on 2019-04-13 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_customer_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='changed_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
