# Generated by Django 3.0.5 on 2021-07-20 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20210720_1945'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favorite',
            name='favorite_recipe',
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'favorite_recipe'), name='unique_favorite_recipe'),
        ),
    ]