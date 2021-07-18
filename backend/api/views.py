from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError
from .models import Ingredient, Recipe, Tag
from .serializers import (
    IngredientSerializer,
    TagSerializer,
    RecipeSerializer,
    FollowSerializer,
)
from django.contrib.auth import get_user_model

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
    filterset_fields = ["is_favorited"]

    # def perform_create(self, serializer):
    #     recipe_id = self.kwargs.get("recipe_id")
    #     get_object_or_404(Recipe, pk=recipe_id)
    #     serializer.save(author=self.request.user, recipe_id=recipe_id)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    # search_fields = ["=following__username", "=user__username"]
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        user = self.request.user
        return user.following.all()

    def perform_create(self, serializer):
        current_user = self.request.user
        following = User.objects.get(id=self.kwargs["user_id"])

        if current_user != following:
            return serializer.save(user=current_user, following=following)
        raise ValidationError("Нельзя подписаться на самого себя")
