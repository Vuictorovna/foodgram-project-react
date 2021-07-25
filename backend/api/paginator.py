from rest_framework.pagination import LimitOffsetPagination


class ResultsSetPagination(LimitOffsetPagination):
    offset_query_param = "page"
