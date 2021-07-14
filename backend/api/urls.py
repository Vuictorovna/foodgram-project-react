from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter


from .views import IngredientViewSet, TagViewSet, RecipeViewSet

router = DefaultRouter()

router.register("ingredients", IngredientViewSet)
router.register(
    r"ingredients/(?P<ingredient_id>\d+)/",
    IngredientViewSet,
    basename="ingredients",
)
router.register("tags", TagViewSet)
router.register(
    r"tags/(?P<tag_id>\d+)/",
    TagViewSet,
    basename="tags",
)
router.register("recipes", RecipeViewSet)
router.register(
    r"recipes/(?P<ingredient_id>\d+)/",
    RecipeViewSet,
    basename="recipes",
)
urlpatterns = [
    path("", include(router.urls)),]
