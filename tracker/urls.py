from django.urls import path
from tracker.apps import TrackerConfig
from tracker.views import TaskViewSet, EmployeeViewSet
from rest_framework.routers import DefaultRouter


app_name = TrackerConfig.name


router = DefaultRouter()
router.register(r'task', TaskViewSet, basename='task')
router.register(r'employee', EmployeeViewSet, basename='employee')

task_create = TaskViewSet.as_view({"post": "create"})
task_detail = TaskViewSet.as_view({"get": "retrieve"})
task_update = TaskViewSet.as_view({"put": "update", "patch": "partial_update"})
task_delete = TaskViewSet.as_view({"delete": "destroy"})

employee_create = EmployeeViewSet.as_view({"post": "create"})
employee_detail = EmployeeViewSet.as_view({"get": "retrieve"})
employee_update = EmployeeViewSet.as_view({"put": "update", "patch": "partial_update"})
employee_delete = EmployeeViewSet.as_view({"delete": "destroy"})

urlpatterns = [
    path('create/', task_create, name='task_create'),
    path('<int:pk>/', task_detail, name='task_detail'),
    path('<int:pk>/update/', task_update, name='task_update'),
    path('<int:pk>/delete/', task_delete, name='task_delete'),

    path('create/', EmployeeViewSet.as_view({"post": "create"}), name='employee_create'),
    path('<int:pk>/', EmployeeViewSet.as_view({"get": "retrieve"}), name='employee_detail'),
    path('<int:pk>/update/', EmployeeViewSet.as_view({"put": "update", "patch": "partial_update"}), name='employee_update'),
    path('<int:pk>/delete/', EmployeeViewSet.as_view({"delete": "destroy"}), name='employee_delete'),
] + router.urls
