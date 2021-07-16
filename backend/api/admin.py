from django.contrib import admin
from api.models import Ingredient, Tag, Recipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "measurement_unit",
    )
    list_filter = ("name",)
    empty_value_display = "-empty-"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    list_filter = ("name", "author", "tags")
    empty_value_display = "-empty-"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    empty_value_display = "-empty-"
