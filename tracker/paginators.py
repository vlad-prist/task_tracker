from rest_framework import pagination


class EmployeePaginator(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10


class TaskPaginator(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10