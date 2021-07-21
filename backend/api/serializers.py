from django.contrib.auth import get_user_model
from django.http import request
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.validators import UniqueTogetherValidator

from .models import (
    Favorite,
    Ingredient,
    Tag,
    Recipe,
    IngredientInRecipe,
    Follow,
)
from users.serializers import UserSerializer

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="ingredients.id")
    amount = serializers.IntegerField(source="ingredients.amount")

    class Meta:
        model = IngredientInRecipe
        fields = ("id", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )
    ingredients = IngredientInRecipeSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()

    def create(self, validated_data):
        print(validated_data)
        # Уберем список достижений из словаря validated_data и сохраним его
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        user = self.context["request"].user

        # Создадим нового котика пока без достижений, данных нам достаточно
        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.tags.set(tags)
        # # Для каждого достижения из списка достижений
        for ingredient in ingredients:
            print(ingredient)
            # Создадим новую запись или получим существующий экземпляр из БД
            current_ingredient = get_object_or_404(
                Ingredient, pk=ingredient["ingredients"]["id"]
            )
            # Поместим ссылку на каждое достижение во вспомогательную таблицу
            # Не забыв указать к какому котику оно относится
            IngredientInRecipe.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient["ingredients"]["amount"],
            )
        return recipe

    class Meta:
        model = Recipe
        fields = ("author", "ingredients", "is_favorited")

    def get_is_favorited(self, obj):
        request = self.context["request"]
        user = request.user
        if user.is_anonymous:
            return False

        favorited = user.favorite_recipes.filter(favorite_recipe=obj)
        if len(favorited) == 0:
            return False
        return True


class RecipiesFromFollowingSerializer(RecipeSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "cooking_time")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class FollowSerializer(UserSerializer):
    email = serializers.EmailField(source="following.email", read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source="following.id", read_only=True
    )
    username = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )
    first_name = serializers.CharField(
        source="following.first_name", read_only=True
    )
    last_name = serializers.CharField(
        source="following.last_name", read_only=True
    )
    recipes = RecipiesFromFollowingSerializer(
        source="following.recipes", many=True, read_only=True
    )
    recipes_count = serializers.IntegerField(
        source="following.recipes.count", read_only=True
    )
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = [
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        ]

    def get_is_subscribed(self, obj):
        subscribed = obj.user.follower.filter(following=obj.following)
        if len(subscribed) == 0:
            return False
        return True


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source="favorite_recipe.id", read_only=True
    )
    name = serializers.CharField(source="favorite_recipe.name", read_only=True)
    cooking_time = serializers.IntegerField(
        source="favorite_recipe.cooking_time", read_only=True
    )

    class Meta:
        model = Favorite
        fields = ("id", "name", "cooking_time")
