from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "role",
        ]
        model = get_user_model()
