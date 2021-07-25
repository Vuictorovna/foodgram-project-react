from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, permissions
from rest_framework.exceptions import ValidationError
from .models import Favorite, Follow, Ingredient, Recipe, ShoppingCart, Tag
from .serializers import (
    IngredientSerializer,
    TagSerializer,
    RecipeSerializer,
    FollowSerializer,
    FavoriteRecipeSerializer,
    ShoppingCartSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from api.paginator import ResultsSetPagination
import io


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
    pagination_class = ResultsSetPagination
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = (
        "author",
        "tags__slug",
    )

    def get_queryset(self):
        user = self.request.user
        is_favorited = self.request.query_params.get("is_favorited")
        is_in_shopping_cart = self.request.query_params.get(
            "is_in_shopping_cart"
        )
        if is_favorited is None and is_in_shopping_cart is None:
            return Recipe.objects.all()

        if is_favorited == "1":
            favorites = []
            recipes = user.favorite_recipes.all()
            for recipe in recipes:
                fav = recipe.favorite_recipe
                favorites.append(fav)
            return favorites

        if is_in_shopping_cart == "1":
            cart = []
            recipes = user.in_cart.all()
            for recipe in recipes:
                rec = recipe.recipe_in_cart
                cart.append(rec)
            return cart


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()

    def perform_create(self, serializer):
        current_user = self.request.user
        following = User.objects.get(id=self.kwargs["user_id"])

        if current_user != following:
            return serializer.save(user=current_user, following=following)
        raise ValidationError("Нельзя подписаться на самого себя")

    @action(
        detail=False,
        methods=["DELETE"],
    )
    def delete(self, request, user_id=None):
        if request.method == "DELETE":
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
        recipe = Recipe.objects.get(id=self.kwargs["recipe_id"])
        return serializer.save(user=current_user, favorite_recipe=recipe)

    @action(
        detail=False,
        methods=["DELETE"],
    )
    def delete(self, request, recipe_id=None):
        if request.method == "DELETE":
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
        recipe = Recipe.objects.get(id=self.kwargs["recipe_id"])
        return serializer.save(user=current_user, recipe_in_cart=recipe)

    @action(
        detail=False,
        methods=["DELETE"],
    )
    def delete(self, request, recipe_id=None):
        if request.method == "DELETE":
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
    s = str(result)
    b = io.BytesIO(s.encode("utf-8"))
    return FileResponse(b, as_attachment=True, filename="list.txt")
