from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название ингредиента",
        help_text="Укажите название ингредиента",
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="Единицы измерения",
        help_text="Укажите единицы измерения",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    GREEN = "#7BFFB8"
    PINK = "#F399C5"
    YELLOW = "#F3F255"
    COLOR_CHOICES = [
        (WHITE, "#FFFFFF"),
        (BLACK, "#000000"),
        (GREEN, "#7BFFB8"),
        (PINK, "#F399C5"),
        (YELLOW, "#F3F255"),
    ]
    name = models.CharField(
        max_length=200,
        verbose_name="Тег",
        help_text="Добавьте тег",
    )
    slug = models.SlugField(max_length=40, unique=True)
    color = ColorField(choices=COLOR_CHOICES, verbose_name="Цвет тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Название рецепта",
        help_text="Укажите название рецепта",
    )
    image = models.ImageField(
        upload_to="image/", verbose_name="Изображение блюда"
    )
    text_description = models.TextField(
        verbose_name="Описание рецепта",
        help_text="Добавьте описание рецепта",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientInRecipe",
        verbose_name="Ингредиенты",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        related_name="recipes",
        verbose_name="Теги",
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления в минутах",
        help_text="Укажите время приготовления в минутах",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации"
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент, используемый в рецепте",
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Рецепт"
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество ингредиента"
    )

    class Meta:
        verbose_name = "Количество ингредиента в рецепте"
        verbose_name_plural = "Количество ингредиентов в рецепте"


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="На кого подписан",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user", "following"], name="unique_follow"
            ),
        ]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite_recipes",
        verbose_name="Пользователь",
    )
    favorite_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorited_by",
        verbose_name="Избранное",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user", "favorite_recipe"],
                name="unique_favorite_recipe",
            ),
        ]
        verbose_name = "Список избранного"
        verbose_name_plural = "Списки избранного"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="in_cart",
        verbose_name="Пользователь",
    )
    recipe_in_cart = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="put_in_cart_by",
        verbose_name="Рецепт в списке покупок",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user", "recipe_in_cart"],
                name="unique_recipe_in_cart",
            ),
        ]
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
