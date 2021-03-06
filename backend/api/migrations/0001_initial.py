import colorfield.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Favorite",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "Список избранного",
                "verbose_name_plural": "Списки избранного",
            },
        ),
        migrations.CreateModel(
            name="Follow",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "Подписка",
                "verbose_name_plural": "Подписки",
            },
        ),
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Укажите название ингредиента",
                        max_length=200,
                        verbose_name="Название ингредиента",
                    ),
                ),
                (
                    "measurement_unit",
                    models.CharField(
                        help_text="Укажите единицы измерения",
                        max_length=200,
                        verbose_name="Единицы измерения",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ингредиент",
                "verbose_name_plural": "Ингредиенты",
            },
        ),
        migrations.CreateModel(
            name="IngredientInRecipe",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.PositiveSmallIntegerField(
                        verbose_name="Количество ингредиента"
                    ),
                ),
            ],
            options={
                "verbose_name": "Количество ингредиента в рецепте",
                "verbose_name_plural": "Количество ингредиентов в рецепте",
            },
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Укажите название рецепта",
                        max_length=200,
                        verbose_name="Название рецепта",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="image/", verbose_name="Изображение блюда"
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Добавьте описание рецепта",
                        verbose_name="Описание рецепта",
                    ),
                ),
                (
                    "cooking_time",
                    models.PositiveSmallIntegerField(
                        help_text="Укажите время приготовления в минутах",
                        verbose_name="Время приготовления в минутах",
                    ),
                ),
                (
                    "pub_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата публикации"
                    ),
                ),
            ],
            options={
                "verbose_name": "Рецепт",
                "verbose_name_plural": "Рецепты",
                "ordering": ["-pub_date"],
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Добавьте тег",
                        max_length=200,
                        verbose_name="Тег",
                    ),
                ),
                ("slug", models.SlugField(max_length=40, unique=True)),
                (
                    "color",
                    colorfield.fields.ColorField(
                        choices=[
                            ("#FFFFFF", "#FFFFFF"),
                            ("#000000", "#000000"),
                            ("#7BFFB8", "#7BFFB8"),
                            ("#F399C5", "#F399C5"),
                            ("#F3F255", "#F3F255"),
                        ],
                        default="#FFFFFF",
                        max_length=18,
                        verbose_name="Цвет тега",
                    ),
                ),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
            },
        ),
        migrations.CreateModel(
            name="ShoppingCart",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "recipe_in_cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="put_in_cart_by",
                        to="api.Recipe",
                        verbose_name="Рецепт в списке покупок",
                    ),
                ),
            ],
            options={
                "verbose_name": "Список покупок",
                "verbose_name_plural": "Списки покупок",
            },
        ),
    ]
