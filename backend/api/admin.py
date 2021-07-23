from django.contrib import admin
from api.models import (
    Ingredient,
    Tag,
    Recipe,
    IngredientInRecipe,
    ShoppingCart,
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "measurement_unit",
    )
    list_filter = ("name",)
    empty_value_display = "-empty-"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # inlines = [IngredientInRecipe]
    list_display = ("id", "name", "author")
    list_filter = ("name", "author", "tags")
    empty_value_display = "-empty-"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    empty_value_display = "-empty-"


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "recipe", "amount")
    empty_value_display = "-empty-"


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "recipe_in_cart")
    empty_value_display = "-empty-"
