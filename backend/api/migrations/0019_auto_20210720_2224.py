# Generated by Django 3.0.5 on 2021-07-20 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0018_recipe_ingredients"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="favorite",
            name="unique_favorite_recipe",
        ),
    ]
