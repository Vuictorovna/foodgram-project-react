from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter


from .views import IngredientViewSet, TagViewSet, RecipeViewSet, FollowViewSet

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
router.register(r"recipes", RecipeViewSet)
router.register(
    r"recipes/(?P<ingredient_id>\d+)/favorite",
    RecipeViewSet,
    basename="recipes",
)
router.register(
    r"users/subscriptions", FollowViewSet, basename="subscriptions"
)
router.register(
    r"users/(?P<user_id>\d+)/subscribe",
    FollowViewSet,
    basename="subscriptions",
)

urlpatterns = [
    path("", include(router.urls)),
]
