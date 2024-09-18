from tracker.models import Employee, Task
from rest_framework import serializers


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "name", "department",)


class TaskSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(format='%d.%m.%Y %H:%M', input_formats=['%d.%m.%Y %H:%M'])

    class Meta:
        model = Task
        fields = ("id", "name", "related_task", "description", "employee", "deadline", "status",)
