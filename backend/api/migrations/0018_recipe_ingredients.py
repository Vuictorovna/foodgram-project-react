# Generated by Django 3.0.5 on 2021-07-20 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20210720_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(blank=True, related_name='ingredients', through='api.IngredientInRecipe', to='api.Ingredient', verbose_name='Ингредиенты'),
        ),
    ]