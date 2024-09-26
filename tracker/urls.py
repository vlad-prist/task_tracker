from django.urls import path
from tracker.apps import TrackerConfig
from tracker.views import TaskViewSet, EmployeeViewSet, EmpListAPIView, TaskOrderingListAPIView, TaskEmptyListAPIView, EmployeesBusy, EmpsFreeForTask, EmployeeTaskListAPIView
from rest_framework.routers import DefaultRouter


app_name = TrackerConfig.name


router = DefaultRouter()
router.register(r'task', TaskViewSet, basename='task')
router.register(r'employee', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('task/list/', TaskOrderingListAPIView.as_view(), name='tasks_list'),
    path('task/empty/', TaskEmptyListAPIView.as_view(), name='task-empty'),

    path('employee/list/', EmpListAPIView.as_view(), name='employees_list'),
    path('employee/busy/', EmployeesBusy.as_view(), name='employees_busy'),
    path('employee/free/', EmpsFreeForTask.as_view(), name='employees_free'),
    path('employee/taskbusy/', EmployeeTaskListAPIView.as_view(), name='employees_task_busy'),
] + router.urls
