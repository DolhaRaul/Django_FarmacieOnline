# Generated by Django 4.1.7 on 2023-03-05 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FarmacieOnline', '0002_alter_medicament_options_tranzactie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tranzactie',
            name='data_tranzactie',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]