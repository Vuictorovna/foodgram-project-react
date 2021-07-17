from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter()

router.register("users", UserViewSet)
# router.register(
#     r"users/(?P<user_id>\d+)/",
#     UserViewSet,
#     basename="users",
# )
urlpatterns = [
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
