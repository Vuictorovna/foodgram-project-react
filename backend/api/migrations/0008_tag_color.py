# Generated by Django 3.0.5 on 2021-07-16 12:23

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_recipe_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(choices=[('#FFFFFF', 'white'), ('#000000', 'black')], default='#FFFFFF', max_length=18),
        ),
    ]