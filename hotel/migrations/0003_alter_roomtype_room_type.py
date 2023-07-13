# Generated by Django 4.2.2 on 2023-07-13 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_alter_roomtype_room_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomtype',
            name='room_type',
            field=models.CharField(choices=[('standard', 'Standard Room'), ('deluxe', 'Deluxe Room'), ('suite', 'Suite Room'), ('executive', 'Executive Room'), ('family', 'Family Room'), ('penthouse', 'Penthouse Suite')], max_length=15, unique=True),
        ),
    ]