# Generated by Django 4.2.4 on 2023-08-29 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botbackend', '0006_alter_card_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatusers',
            options={'ordering': ['name']},
        ),
        migrations.AddIndex(
            model_name='chatusers',
            index=models.Index(fields=['name'], name='botbackend__name_c138ce_idx'),
        ),
    ]
