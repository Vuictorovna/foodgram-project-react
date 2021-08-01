from django_filters import CharFilter, FilterSet, ModelMultipleChoiceFilter
from rest_framework import filters

from .models import Ingredient, Recipe, Tag


def is_param_enabled(value):
    if value == "1" or value == "true":
        return True
    return False


class RecipeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        is_favorited = request.query_params.get("is_favorited")
        is_in_shopping_cart = request.query_params.get("is_in_shopping_cart")

        if is_param_enabled(is_favorited):
            favorited = queryset.filter(favorited_by__user=user)
            return favorited

        if is_param_enabled(is_in_shopping_cart):
            cart = queryset.filter(put_in_cart_by__user=user)
            return cart

        return queryset


class IngredientFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="startswith")

    class Meta:
        model = Ingredient
        fields = ("name",)


class RecipeFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ("author",)
