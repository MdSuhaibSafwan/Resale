from rest_framework.pagination import PageNumberPagination


class Results1000SetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'


class Results100SetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'


class Results10SetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class Results20SetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
