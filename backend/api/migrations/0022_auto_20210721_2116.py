# Generated by Django 3.0.5 on 2021-07-21 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20210720_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(blank=True, through='api.IngredientInRecipe', to='api.Ingredient', verbose_name='Ингредиенты'),
        ),
    ]
