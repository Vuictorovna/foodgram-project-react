from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from .permissions import IsAdminRole
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminRole]
    lookup_field = "username"
    # pagination_class = PageNumberPagination

    @action(
        detail=False,
        # permission_classes=[IsAuthenticated],
        methods=["GET", "PATCH"],
    )
    def me(self, request):
        if request.method == "GET":
            serializer = UserSerializer(instance=request.user)
            return Response(serializer.data)

        if request.method == "PATCH":
            serializer = UserSerializer(
                instance=request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

