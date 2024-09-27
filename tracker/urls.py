from django.urls import path
from tracker.apps import TrackerConfig
from tracker.views import (
    TaskViewSet,
    EmployeeViewSet,
    TaskListAPIView,
    ImportantTaskList,
    EmployeeTaskListAPIView,
)
from rest_framework.routers import DefaultRouter
from tracker.models import Task

app_name = TrackerConfig.name


router = DefaultRouter()
router.register(r"task", TaskViewSet, basename="task")
router.register(r"employee", EmployeeViewSet, basename="employee")

urlpatterns = [
    # Запрашивает из БД список всех задач.
    path("task/list/", TaskListAPIView.as_view(), name="tasks_list"),
    # Запрашивает из БД список задач без сотрудника.
    path(
        "task/list/empty/",
        TaskListAPIView.as_view(queryset=Task.objects.filter(employee=None)),
        name="task_list_empty",
    ),
    # Запрашивает из БД список всех занятых сотрудников.
    path(
        "employee/busy/", EmployeeTaskListAPIView.as_view(), name="employees_task_busy"
    ),
    # Запрашивает из БД список сотрудников для задач с высоким приоритетом.
    path(
        "employee/available/",
        ImportantTaskList.as_view(),
        name="employees_available_list",
    ),
] + router.urls
