from rest_framework import serializers

from .models import Ingredient, Tag, Recipe, IngredientInRecipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="ingredients.id")

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
        # Уберем список достижений из словаря validated_data и сохраним его
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        # Создадим нового котика пока без достижений, данных нам достаточно
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        # Для каждого достижения из списка достижений
        for ingredient in ingredients:
            # Создадим новую запись или получим существующий экземпляр из БД
            current_igredient, status = Ingredient.objects.get_or_create(
                **ingredient
            )
            # Поместим ссылку на каждое достижение во вспомогательную таблицу
            # Не забыв указать к какому котику оно относится
            IngredientInRecipe.objects.create(
                igredient=current_igredient, recipe=recipe
            )
        return recipe

    class Meta:
        model = Recipe
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
