from rest_framework import filters


class RecipeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        is_favorited = request.query_params.get("is_favorited")
        is_in_shopping_cart = request.query_params.get("is_in_shopping_cart")

        if is_favorited is None and is_in_shopping_cart is None:
            return queryset

        if is_favorited == "1":
            favorited = queryset.filter(favorited_by__user=user)
            return favorited

        if is_in_shopping_cart == "1":
            cart = queryset.filter(put_in_cart_by__user=user)
            return cart
