from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class ExtendedPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })

class PaginationFilter():
    def filter_page_size(self, queryset, name, value):
        if value is not None:
            queryset = queryset[:value]
        return queryset