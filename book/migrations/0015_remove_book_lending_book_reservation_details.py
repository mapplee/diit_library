# Generated by Django 3.2 on 2021-04-30 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0014_alter_checkout_details_total_checkout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book_lending',
            name='book_reservation_details',
        ),
    ]
