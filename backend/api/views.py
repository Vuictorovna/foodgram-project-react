from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError
from .models import Favorite, Follow, Ingredient, Recipe, ShoppingCart, Tag
from .serializers import (
    IngredientSerializer,
    TagSerializer,
    RecipeSerializer,
    FollowSerializer,
    FavoriteRecipeSerializer,
    ShoppingCartSerializer,
    ShoppingListSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
import io


User = get_user_model()


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = (
    #     "author",
    #     "tags__slug",
    # )

    # def get_queryset(self):
    #     queryset = Recipe.objects.all()
    #     user = self.request.user
    #     user_id = user.pk
    #     is_favorited = self.request.query_params.get("is_favorited")
    #     # if is_favorited is not None:
    #     #     queryset = queryset.filter(favorited_by=user_id)
    #     #     print(queryset)
    #     favorited = queryset.favorited_by.filter()
    #     print(is_favorited)
    #     # return is_favorited
    # def get_queryset(self):
    #     user = self.request.user
    #     is_favorited = self.request.query_params.get("is_favorited")
    #     print(type(is_favorited))
    #     is_in_shopping_cart = self.request.query_params.get(
    #         "is_in_shopping_cart"
    #     )
    #     if is_favorited is None and is_in_shopping_cart is None:
    #         return Recipe.objects.all()
    #     if is_favorited == "1":
    #         print(user.favorite_recipes.all())
    #         return user.favorite_recipes.all()
    #         recipe = user.favorite_recipes.all()[0]
    #         fav = recipe__favorite_recipe
    #         users = favorite_recipe.favorited_by.all()
    #     if is_in_shopping_cart == 1:
    #         return user.in_cart.all()


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

    # @action(
    #     detail=False,
    #     methods=["PUT"],
    # )
    # def update(self, instance, validated_data):
    #     instance.title = validated_data["title"]
    #     instance.save()
    #     return instance


# class ShoppingListViewSet(viewsets.ViewSet):
#     # serializer_class = ShoppingListSerializer
#     @action(
#         detail=False,
#         methods=["GET"],
#     )
@api_view(["GET"])
def get_list(request):
    # user = request.user
    user = User.objects.get(id=10)
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
    b = io.StringIO(s)
    return FileResponse(b, as_attachment=True, filename="list.txt")
