from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Ingredient",
        help_text="Enter the ingredient name",
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="Measurement Unit",
        help_text="Enter the measurement unit",
    )

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredient"

    def __str__(self):
        return self.name


class Tag(models.Model):
    JASPER = "#C84630"
    ROSY = "#D4A0A7"
    PLATINUM = "#E3E3E3"
    GRAY = "#898989"
    JADE = "#5DA271"
    COLOR_CHOICES = [
        (JASPER, "#C84630"),
        (ROSY, "#D4A0A7"),
        (PLATINUM, "#E3E3E3"),
        (GRAY, "#898989"),
        (JADE, "#5DA271"),
    ]
    name = models.CharField(
        max_length=200,
        verbose_name="Tag",
        help_text="Add tag",
    )
    slug = models.SlugField(max_length=40, unique=True)
    color = ColorField(choices=COLOR_CHOICES, verbose_name="Tag Color")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Author",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Recipe Name",
        help_text="Enter the recipe name",
    )
    image = models.ImageField(
        null=False, upload_to="image/", verbose_name="Dish Image"
    )
    text = models.TextField(
        verbose_name="Recipe Description",
        help_text="Add a description for the recipe",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientInRecipe",
        verbose_name="Ingredients",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        related_name="recipes",
        verbose_name="Tags",
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Cooking Time (minutes)",
        help_text="Enter the cooking time in minutes",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Publication Date"
    )

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ingredient used in recipe",
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Recipe"
    )
    amount = models.PositiveSmallIntegerField(verbose_name="Ingredient amount")

    class Meta:
        verbose_name = "Ingredient amount in recipe"
        verbose_name_plural = "Ingredient amounts in recipe"


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Follower",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Following",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user", "following"], name="unique_follow"
            ),
        ]
        verbose_name = "Follow"
        verbose_name_plural = "Follows"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite_recipes",
        verbose_name="User",
    )
    favorite_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorited_by",
        verbose_name="Favorite Recipe",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user", "favorite_recipe"],
                name="unique_favorite_recipe",
            ),
        ]
        verbose_name = "Favorite Recipe List"
        verbose_name_plural = "Favorite Recipe Lists"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="in_cart",
        verbose_name="User",
    )
    recipe_in_cart = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="put_in_cart_by",
        verbose_name="Recipe in Shopping Cart",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user", "recipe_in_cart"],
                name="unique_recipe_in_cart",
            ),
        ]
        verbose_name = "Shopping Cart"
        verbose_name_plural = "Shopping Carts"
