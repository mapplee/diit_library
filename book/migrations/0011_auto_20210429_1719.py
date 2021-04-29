# Generated by Django 3.2 on 2021-04-29 17:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0010_book_reservation_reserver_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='book_Lending',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField()),
                ('due_date', models.DateTimeField()),
                ('return_date', models.DateTimeField()),
            ],
        ),
        migrations.RenameField(
            model_name='book_reservation',
            old_name='reserved_book',
            new_name='reserved_book_details',
        ),
        migrations.RenameField(
            model_name='book_reservation',
            old_name='reserver_id',
            new_name='reserver_detials',
        ),
        migrations.CreateModel(
            name='fine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(null=True)),
                ('lending_details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='book.book_lending')),
                ('reservation_details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='book.book_reservation')),
            ],
        ),
        migrations.AddField(
            model_name='book_lending',
            name='book_reservation_details',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='book.book_reservation'),
        ),
        migrations.AddField(
            model_name='book_lending',
            name='lender_book_details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.bookitem'),
        ),
        migrations.AddField(
            model_name='book_lending',
            name='lender_details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]