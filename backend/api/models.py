from django.contrib.auth import get_user_model
from django.db import models
from colorfield.fields import ColorField


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        verbose_name="Название ингредиента",
        help_text="Укажите название ингредиента",
    )
    measurement_unit = models.CharField(
        max_length=200,
        blank=False,
        verbose_name="Единицы измерения",
        help_text="Укажите единицы измерения",
    )

    class Meta:
        verbose_name_plural = "Ингредиенты"


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Тэг",
        help_text="Добавьте тэг",
    )
    slug = models.SlugField(max_length=40, unique=True)
    COLOR_CHOICES = [
        ("#FFFFFF", "white"),
        ("#000000", "black"),
        ("#7BFFB8", "green"),
        ("#F399C5", "pink"),
        ("#F3F255", "yellow"),
    ]
    color = ColorField(choices=COLOR_CHOICES)

    class Meta:
        verbose_name_plural = "Тэги"


class Recipe(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    author = models.ForeignKey(
        User,
        blank=True,
        on_delete=models.CASCADE,
        related_name="author",
        verbose_name="Автор рецепта",
    )
    name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Название",
        help_text="Укажите название рецепта",
    )
    # image = models.ImageField(
    #     upload_to='image/',
    #     null=True
    # )
    text_description = models.TextField(
        blank=True,
        verbose_name="Описание рецепта",
        help_text="Добавьте описание рецепта",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=True,
        through="IngredientInRecipe",
        related_name="ingredients",
        verbose_name="Ингредиенты",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="tags",
        verbose_name="Теги",
    )
    cooking_time = models.PositiveSmallIntegerField(
        blank=True,
        verbose_name="Время приготовления в минутах",
        help_text="Укажите время приготовления в минутах",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации"
    )

    # is_favorited = models.BooleanField(
    #     blank=True,
    # )
    # is_in_shopping_cart = models.BooleanField(
    #     blank=True,
    # )

    class Meta:
        verbose_name_plural = "Рецепты"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, blank=False
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, blank=False)
    amount = models.PositiveSmallIntegerField(blank=False)
