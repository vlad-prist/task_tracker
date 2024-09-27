from tracker.models import Employee, Task
from rest_framework import serializers
from tracker.validators import validate_deadline, StatusValidator


class TaskSerializer(serializers.ModelSerializer):
    """ Список всех задач """
    deadline = serializers.DateTimeField(format='%d.%m.%Y %H:%M',
                                         input_formats=['%d.%m.%Y %H:%M'],
                                         validators=[validate_deadline]
                                         )

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "related_task",
            "description",
            "employee",
            "deadline",
            "priority",
            "status",
        )
        validators = [StatusValidator(field_emp="employee", field_status="status"),]

    def update(self, obj, validated_data):
        """ При назначении сотрудника на уже созданную задачу - статус задачи меняется. """
        new_employee = validated_data.get('employee', None)
        if new_employee and obj.status == Task.STATUS_CREATED:
            obj.status = Task.STATUS_IN_PROGRESS
        return super().update(obj, validated_data)


class TaskShortListSerializer(serializers.ModelSerializer):
    """ Краткая информация о задачах. """
    deadline = serializers.DateTimeField(format='%d.%m.%Y %H:%M',
                                         input_formats=['%d.%m.%Y %H:%M'],
                                         validators=[validate_deadline]
                                         )

    class Meta:
        model = Task
        fields = ("id",
                  "title",
                  "related_task",
                  "description",
                  "deadline",
                  "priority",
                  "status",
                  )


class EmployeeSerializer(serializers.ModelSerializer):
    """ Список всех сотрудников. """
    list_tasks = TaskShortListSerializer(source='task', many=True)
    total_tasks_count = serializers.SerializerMethodField()
    active_tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            "id",
            "name",
            "position",
            "department",
            "active_tasks_count",
            "total_tasks_count",
            "list_tasks",
        )

    def get_total_tasks_count(self, obj):
        """ Общие число задач. """
        return obj.task.count()

    def get_active_tasks_count(self, obj):
        """ Задачи в работе. """
        return obj.task.filter(status=Task.STATUS_IN_PROGRESS).count()


class EmployeeActiveTaskSerializer(serializers.ModelSerializer):
    #working
    """ Список сотрудников с активными задачами. """
    active_tasks_count = serializers.SerializerMethodField()
    active_tasks_list = serializers.SerializerMethodField()
    total_tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            "id",
            "name",
            "position",
            "department",
            "total_tasks_count",
            "active_tasks_count",
            "active_tasks_list",
        )

    def get_active_tasks_count(self, obj):
        """ Задачи в работе. """
        return obj.task.filter(status=Task.STATUS_IN_PROGRESS).count()

    def get_total_tasks_count(self, obj):
        """ Общие число задач. """
        return obj.task.count()

    def get_active_tasks_list(self, obj):
        """ Список задач в работе. """
        data = obj.task.filter(status=Task.STATUS_IN_PROGRESS)
        new_data = TaskShortListSerializer(data=data, many=True)
        new_data.is_valid()
        return new_data.data
