from rest_framework.pagination import LimitOffsetPagination


class ResultsSetPagination(LimitOffsetPagination):
    page_size = 1
    offset_query_param = "page"
