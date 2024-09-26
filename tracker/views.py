from datetime import timedelta

from django.db.models import Count, Q, Min
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from tracker.models import Task, Employee
from tracker.serializers import EmployeeSerializer, TaskSerializer, EmployeeActiveTaskSerializer
from tracker.paginators import EmployeePaginator, TaskPaginator


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('deadline')
    serializer_class = TaskSerializer
    pagination_class = TaskPaginator

    def perform_create(self, serializer):
        task = serializer.save()
        task.save()
        return task


class TaskOrderingListAPIView(generics.ListAPIView):
    """ Запрашивает из БД список всех задач, отсортированных по дате окончания срока выполнения. """
    serializer_class = TaskSerializer
    queryset = Task.objects.all().order_by('deadline')
    pagination_class = TaskPaginator
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('status', 'deadline', 'employee')


class TaskEmptyListAPIView(generics.ListAPIView):
    """ Запрашивает из БД список задач без сотрудника. """
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(employee=None)
    pagination_class = TaskPaginator


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = EmployeePaginator

    def perform_create(self, serializer):
        employee = serializer.save()
        employee.save()
        return employee


class EmpListAPIView(generics.ListAPIView):
    """ Запрашивает из БД список всех сотрудников и их задачи, отсортированных по роли и отделу. """
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all().order_by('department')
    pagination_class = EmployeePaginator
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('position', 'department')


class EmployeesBusy(APIView):
    """ 1. Запрашивает из БД список сотрудников и их задачи, отсортированные по количеству активных задач. """

    def get(self, request, *args, **kwargs):
        employee_queryset = Employee.objects.annotate(
            task_count=Count('task')
        ).filter(task_count__gt=0, task__status='in_progress').order_by('-task_count')
        employee_serializer = EmployeeSerializer(employee_queryset, many=True)
        return Response(employee_serializer.data)
    # не работает фильтр по задачам в работе.


class EmployeeTaskListAPIView(generics.ListAPIView):
    # working
    queryset = Employee.objects.all()
    serializer_class = EmployeeActiveTaskSerializer

    def get_queryset(self):
        return Employee.objects.annotate(
            active_tasks_count=Count("task", filter=Q(task__status="in_progress"))
        ).filter(active_tasks_count__gt=0).order_by("-active_tasks_count")


class EmpsFreeForTask(APIView):
    """ Реализует поиск по сотрудникам, которые могут взять такие задачи
    (наименее загруженный сотрудник или сотрудник, выполняющий родительскую задачу,
    если ему назначено максимум на 2 задачи больше, чем у наименее загруженного сотрудника). """

    def get(self, request, *args, **kwargs):
        # Запрашивает из БД задачи, которые не взяты в работу, но от которых зависят другие задачи, взятые в работу.
        upcoming_deadline = timezone.now() + timedelta(days=3) # Ближайшие на три дня задачи
        task_queryset = Task.objects.filter(
            employee=None,
            related_task__employee__isnull=False,
            deadline__lte=upcoming_deadline
        )
        # Поиск по сотрудникам, которые могут взять такие задачи
        employee_queryset = Employee.objects.annotate(tasks_count=Count('task'))
        min_task_count = employee_queryset.aggregate(Min('tasks_count'))['tasks_count__min']
        available_employees = Employee.objects.annotate(tasks_count=Count('task')).filter(
            Q(tasks_count=min_task_count) |  # Условие 1: наименее загруженный сотрудник
            Q(tasks_count__lte=min_task_count + 2, task__related_task__isnull=False)
            # Условие 2: сотрудник с родительской задачей и с разницей задач не более 2
        ).distinct()
        employee_serializer = EmployeeSerializer(available_employees, many=True)
        task_serializer = TaskSerializer(task_queryset, many=True)
        # return Response({'employees': employee_serializer.data, 'tasks': task_serializer.data})
        list_of_task = []
        for one_task in task_queryset:
            list_of_task.append({
                'Important task': one_task.title,
                'Deadline': one_task.deadline,
                'Employees': employee_serializer.data,
            })
        return Response(list_of_task)
