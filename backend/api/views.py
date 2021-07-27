import io

from django.contrib.auth import get_user_model
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view

from rest_framework.response import Response
from .filters import RecipeFilterBackend

from .models import Favorite, Follow, Ingredient, Recipe, ShoppingCart, Tag
from .serializers import (
    FavoriteRecipeSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipeSerializer,
    ShoppingCartSerializer,
    TagSerializer,
)

User = get_user_model()


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("name",)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    filter_backends = [DjangoFilterBackend, RecipeFilterBackend]
    filterset_fields = (
        "author",
        "tags__slug",
    )


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()

    def perform_create(self, serializer):
        current_user = self.request.user
        following = get_object_or_404(User, id=self.kwargs["user_id"])
        return serializer.save(user=current_user, following=following)

    @action(
        detail=False,
        methods=["DELETE"],
    )
    def delete(self, request, user_id=None):
        current_user = request.user
        following = get_object_or_404(User, id=user_id)
        get_object_or_404(
            Follow, user=current_user, following=following
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteRecipeSerializer

    def get_queryset(self):
        user = self.request.user
        return user.favorite_recipes.all()

    def perform_create(self, serializer):
        current_user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs["recipe_id"])
        return serializer.save(user=current_user, favorite_recipe=recipe)

    @action(
        detail=False,
        methods=["DELETE"],
    )
    def delete(self, request, recipe_id=None):
        current_user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        get_object_or_404(
            Favorite, user=current_user, favorite_recipe=recipe
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        user = self.request.user
        cart = user.in_cart.all()
        result = {}
        for recipe in cart:
            ingredients = recipe.recipe_in_cart.ingredientinrecipe_set.all()
            for ingredient in ingredients:
                amount_in_cart = ingredient.amount
                ingredient_in_cart_id = ingredient.ingredient.id
                if ingredient_in_cart_id in result:
                    result[ingredient_in_cart_id] += amount_in_cart
                else:
                    result[ingredient_in_cart_id] = amount_in_cart

        return result

    def perform_create(self, serializer):
        current_user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs["recipe_id"])
        return serializer.save(user=current_user, recipe_in_cart=recipe)

    @action(
        detail=False,
        methods=["DELETE"],
    )
    def delete(self, request, recipe_id=None):
        current_user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        get_object_or_404(
            ShoppingCart, user=current_user, recipe_in_cart=recipe
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def get_list(request):
    user = request.user
    cart = user.in_cart.all()
    result = {}
    for recipe in cart:
        ingredients = recipe.recipe_in_cart.ingredientinrecipe_set.all()
        for ingredient in ingredients:
            amount_in_cart = ingredient.amount
            ingredient_in_cart_id = ingredient.ingredient.id
            if ingredient_in_cart_id in result:
                result[ingredient_in_cart_id] += amount_in_cart
            else:
                result[ingredient_in_cart_id] = amount_in_cart
    ingredients_list = str(result)
    ingredients_list_bytes = io.BytesIO(ingredients_list.encode("utf-8"))
    return FileResponse(
        ingredients_list_bytes, as_attachment=True, filename="list.txt"
    )
