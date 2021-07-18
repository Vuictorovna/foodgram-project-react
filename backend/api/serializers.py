from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator

from .models import Ingredient, Tag, Recipe, IngredientInRecipe, Follow

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
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
        required=False,
    )
    following = serializers.SlugRelatedField(
        slug_field="username", read_only=True, required=False
    )

    class Meta:
        fields = "__all__"
        model = Follow
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Follow.objects.all(), fields=["user", "following"]
        #     )
        # ]

    def validate(self, data):
        print("hello!", data)
        if self.context["request"].user.id != data.get("user_id"):
            return data
        raise serializers.ValidationError("Нельзя подписаться на самого себя")
