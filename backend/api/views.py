from django.db.models import query
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError
from .models import Favorite, Follow, Ingredient, Recipe, Tag
from .serializers import (
    IngredientSerializer,
    TagSerializer,
    RecipeSerializer,
    FollowSerializer,
    FavoriteRecipeSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status


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
    # filterset_fields = ["is_favorited"]

    # def perform_create(self, serializer):
    #     recipe_id = self.kwargs.get("recipe_id")
    #     get_object_or_404(Recipe, pk=recipe_id)
    #     serializer.save(author=self.request.user, recipe_id=recipe_id)


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
        print("!!!!!!!!")
        current_user = self.request.user
        recipe = Recipe.objects.get(id=self.kwargs["recipe_id"])
        return serializer.save(user=current_user, favorite_recipe=recipe)

    @action(
        detail=False,
        methods=["DELETE"],
    )
    def delete(self, request, recipe_id=None):
        print("!!!!!!!!")
        if request.method == "DELETE":
            current_user = request.user
            recipe = get_object_or_404(Recipe, id=recipe_id)
            get_object_or_404(
                Favorite, user=current_user, favorite_recipe=recipe
            ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
