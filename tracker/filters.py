from django_filters import rest_framework as filters
from tracker.models import Task


class TaskDateFilter(filters.FilterSet):
    exact_deadline = filters.DateFilter(field_name="deadline", lookup_expr='exact')

    class Meta:
        model = Task
        fields = ['deadline'] # чтобы фильтр заработал, в модели у deadline должно быть поле DateField
