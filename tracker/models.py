from django.db import models

NULLABLE = {"blank": True, "null": True}


class BaseModel(models.Model):
    objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="время последнего изменения")

    class Meta:
        abstract = True


class Task(BaseModel):
    STATUS_CREATED = 'created'
    STATUS_ASSIGNED = 'assigned'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_FINISHED = 'finished'

    STATUS_CHOICES = (
        (STATUS_CREATED, 'Создана'),
        (STATUS_ASSIGNED, 'Назначен исполнитель'),
        (STATUS_IN_PROGRESS, 'В работе'),
        (STATUS_FINISHED, 'Завершена'),
    )

    name = models.CharField(max_length=300, verbose_name='Название задачи')
    related_task = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name="Связанная задача", **NULLABLE)
    description = models.TextField(verbose_name='Описание задачи')
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, verbose_name='Сотрудник', **NULLABLE)
    deadline = models.DateTimeField(auto_now_add=False, verbose_name='Срок выполнения', help_text='ДД.ММ.ГГГГ 00:00')
    status = models.CharField(max_length=100, verbose_name='Статус задачи', choices=STATUS_CHOICES, default=STATUS_CREATED)

    def __str__(self):
        return self.name, self.description

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Employee(BaseModel):
    name = models.CharField(max_length=100, verbose_name='ФИО сотрудника')
    position = models.CharField(max_length=100, verbose_name='Должность сотрудника')
    department = models.CharField(max_length=100, verbose_name='Отдел сотрудника', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
