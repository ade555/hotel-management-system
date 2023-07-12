# Generated by Django 4.2.2 on 2023-07-12 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomtype',
            name='room_type',
            field=models.CharField(choices=[('standard', 'Standard Room'), ('deluxe', 'Deluxe Room'), ('suite', 'Suite'), ('executive', 'Executive Room'), ('family', 'Family Room'), ('penthouse', 'Penthouse Suite')], max_length=15, unique=True),
        ),
    ]
