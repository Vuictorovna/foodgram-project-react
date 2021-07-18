from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter()

router.register("users", UserViewSet)

urlpatterns = [
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
