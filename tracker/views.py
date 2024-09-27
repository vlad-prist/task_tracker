from django.db.models import Count, Q, Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from tracker.models import Task, Employee
from tracker.serializers import (
    EmployeeSerializer,
    TaskSerializer,
    EmployeeActiveTaskSerializer,
)
from tracker.paginators import EmployeePaginator, TaskPaginator


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("deadline")
    serializer_class = TaskSerializer
    pagination_class = TaskPaginator

    def perform_create(self, serializer):
        task = serializer.save()
        task.save()
        return task


class TaskListAPIView(generics.ListAPIView):
    """Запрашивает из БД список всех задач, отсортированных по дате окончания срока выполнения."""

    serializer_class = TaskSerializer
    queryset = Task.objects.all().order_by("deadline")
    pagination_class = TaskPaginator
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("status", "deadline", "employee")


class EmployeeViewSet(viewsets.ModelViewSet):
    """Запрашивает из БД список всех сотрудников, отсортированных по отделу."""

    queryset = Employee.objects.all().order_by("department")
    serializer_class = EmployeeSerializer
    pagination_class = EmployeePaginator

    def perform_create(self, serializer):
        employee = serializer.save()
        employee.save()
        return employee


class EmployeeTaskListAPIView(generics.ListAPIView):
    """
    1. Запрашивает из БД список сотрудников и их задачи, отсортированные по количеству активных задач.
    С возможностью фильтрации по должности и отделу.
    """

    serializer_class = EmployeeActiveTaskSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("position", "department")

    def get_queryset(self):
        return Employee.objects.annotate(
            active_tasks_count=Count("task", filter=Q(task__status="in_progress"))
        ).filter(active_tasks_count__gt=0).order_by("-active_tasks_count")


class ImportantTaskList(APIView):
    """Предоставляет из БД:
    1. задачи, которые не взяты в работу, но от которых зависят другие задачи, взятые в работу.
    2. Поиск сотрудников, которые могут взять найденную задачу в работу:
    2.1. Это могут быть сотрудники с наименьшей загрузкой
    2.2. Или сотрудник с родительской задачей и с разницей задач не более 2.
    """

    def get(self, request, *args, **kwargs):
        # 1. Запрашивает из БД задачи, которые не взяты в работу, но от которых зависят другие задачи, взятые в работу.
        task_queryset = Task.objects.filter(
            employee=None, related_task__employee__isnull=False, priority__iexact="high"
        )
        # Поиск по сотрудникам, которые могут взять такие задачи
        employee_queryset = Employee.objects.annotate(tasks_count=Count("task"))
        min_task_count = employee_queryset.aggregate(Min("tasks_count"))["tasks_count__min"]
        available_employees = Employee.objects.annotate(tasks_count=Count("task")).filter(
            # Условие 1: наименее загруженный сотрудник
            Q(tasks_count=min_task_count)
            |
            # Условие 2: сотрудник с родительской задачей и с разницей задач не более 2
            Q(tasks_count__lte=min_task_count + 2, task__related_task__isnull=False)
        ).distinct()
        employee_serializer = EmployeeSerializer(available_employees, many=True)
        list_of_task = []
        for one_task in task_queryset:
            list_of_task.append(
                {
                    "task_id": one_task.id,
                    "Important task": one_task.title,
                    "Deadline": one_task.deadline.strftime("%d.%m.%Y %H:%M"),
                    "Employees": employee_serializer.data,
                }
            )
        return Response(list_of_task)
