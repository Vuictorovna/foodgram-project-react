from django.conf.urls import include
from django.urls import path, re_path
from rest_framework import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns


from .views import (
    IngredientViewSet,
    TagViewSet,
    RecipeViewSet,
    FollowViewSet,
    FavoriteViewSet,
)

router = DefaultRouter()

router.register(r"ingredients", IngredientViewSet)
router.register(
    r"ingredients/(?P<ingredient_id>\d+)/",
    IngredientViewSet,
    basename="ingredients",
)
router.register(r"tags", TagViewSet)
router.register(
    r"tags/(?P<tag_id>\d+)/",
    TagViewSet,
    basename="tags",
)
router.register(
    r"recipes/(?P<recipe_id>\d+)/favorite",
    FavoriteViewSet,
    basename="favorite",
)
router.register(
    r"recipes/favorite",
    FavoriteViewSet,
    basename="favorite_list",
)
router.register(r"recipes", RecipeViewSet)
router.register(
    r"recipes/(?P<recipe_id>\d+)/",
    RecipeViewSet,
    basename="recipes",
)
router.register(
    r"users/(?P<user_id>\d+)/subscribe",
    FollowViewSet,
    basename="xxxxxx",
)
router.register(
    r"users/subscriptions", FollowViewSet, basename="subscriptions"
)


urlpatterns = [
    path("", include(router.urls)),
]
