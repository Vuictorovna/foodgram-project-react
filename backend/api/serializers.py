from django.contrib.auth import get_user_model
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import (
    Favorite,
    Ingredient,
    ShoppingCart,
    Tag,
    Recipe,
    IngredientInRecipe,
    Follow,
)
from users.serializers import UserSerializer

User = get_user_model()


class AuthorSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        ]

    def get_is_subscribed(self, obj):
        request = self.context["request"]
        user = request.user
        if user.is_anonymous:
            return False
        subscribed = user.follower.filter(following=obj)

        if len(subscribed) == 0:
            return False
        return True


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source="favorite_recipe.id", read_only=True
    )
    name = serializers.CharField(source="favorite_recipe.name", read_only=True)
    image = Base64ImageField(source="favorite_recipe.image", read_only=True)
    cooking_time = serializers.IntegerField(
        source="favorite_recipe.cooking_time", read_only=True
    )

    class Meta:
        model = Favorite
        fields = ("id", "name", "image", "cooking_time")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

    def to_internal_value(self, data):
        return Tag.objects.get(id=data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"

    def to_internal_value(self, data):
        return Ingredient.objects.get(id=data)


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = IngredientSerializer()
    name = serializers.CharField(required=False)
    measurement_unit = serializers.IntegerField(required=False)
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ("id", "amount", "name", "measurement_unit")

    def to_representation(self, instance):
        data = IngredientSerializer(instance.ingredient).data
        data["amount"] = instance.amount
        return data


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = AuthorSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source="ingredientinrecipe_set", many=True
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredientinrecipe_set")
        user = self.context["request"].user
        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            IngredientInRecipe.objects.create(
                ingredient=ingredient["id"],
                recipe=recipe,
                amount=ingredient["amount"],
            )
        return recipe

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text_description",
            "cooking_time",
            "is_favorited",
        )

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
        fields = ("id", "name", "image", "cooking_time")


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


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source="recipe_in_cart.id", read_only=True
    )
    name = serializers.CharField(source="recipe_in_cart.name", read_only=True)
    image = Base64ImageField(source="recipe_in_cart.image", read_only=True)
    cooking_time = serializers.IntegerField(
        source="recipe_in_cart.cooking_time", read_only=True
    )

    class Meta:
        model = ShoppingCart
        fields = ("id", "name", "image", "cooking_time")


class ShoppingListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    measurement_unit = serializers.IntegerField(required=False)
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ("name", "measurement_unit", "amount")

    def to_representation(self, instance):
        data = IngredientSerializer(instance.ingredient).data
        data["amount"] = instance.amount
        return data
