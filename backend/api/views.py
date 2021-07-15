from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Ingredient, Recipe, Tag
from .serializers import IngredientSerializer, TagSerializer, RecipeSerializer

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    # def perform_create(self, serializer):
    #     recipe_id = self.kwargs.get("recipe_id")
    #     get_object_or_404(Recipe, pk=recipe_id)
    #     serializer.save(author=self.request.user, recipe_id=recipe_id)
