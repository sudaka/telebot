# Generated by Django 4.2.4 on 2023-08-28 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('botbackend', '0005_alter_card_pack'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ['pack', 'number']},
        ),
    ]
