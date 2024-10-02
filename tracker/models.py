from django.db import models
from django.utils import timezone

NULLABLE = {"blank": True, "null": True}


class BaseModel(models.Model):
    objects = models.Manager()
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="время создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="время последнего изменения"
    )

    class Meta:
        abstract = True


class Task(BaseModel):
    STATUS_CREATED = "created"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_FINISHED = "finished"
    STATUS_OVERDUE = "overdue"

    STATUS_CHOICES = (
        (STATUS_CREATED, "Создана"),
        (STATUS_IN_PROGRESS, "В работе"),
        (STATUS_FINISHED, "Завершена"),
        (STATUS_OVERDUE, "Просрочена"),
    )

    title = models.CharField(
        max_length=300,
        verbose_name="Название задачи"
    )
    related_task = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная задача",
        **NULLABLE
    )
    description = models.TextField(verbose_name="Описание задачи")
    employee = models.ForeignKey(
        "Employee",
        verbose_name="Сотрудник",
        on_delete=models.SET_NULL,
        related_name="task",
        **NULLABLE
    )
    deadline = models.DateTimeField(
        auto_now_add=False,
        verbose_name="Срок выполнения",
        help_text="ДД.ММ.ГГГГ 00:00"
    )
    status = models.CharField(
        max_length=100,
        verbose_name="Статус задачи",
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
    )
    priority = models.CharField(
        max_length=100,
        verbose_name="Приоритет задачи",
        choices=[
            ("low", "Низкий"),
            ("medium", "Средний"),
            ("high", "Высокий")
        ],
        default="low",
    )

    def __str__(self):
        return self.title, self.description

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def save(self, *args, **kwargs):
        """
        1. При сохранении экземпляра, если указан сотрудник и статус 'created',
        то изменяем статус на 'in_progress'.
        2. Если дедлайн просрочен и статус заявки не 'finished',
        то при обновлении задачи меняется статус на 'overdue'.
        """
        if self.employee and self.status == self.STATUS_CREATED:
            self.status = self.STATUS_IN_PROGRESS
        elif (self.deadline < timezone.now()
              and self.status != self.STATUS_FINISHED):
            self.status = self.STATUS_OVERDUE
        super().save(*args, **kwargs)


class Employee(BaseModel):
    name = models.CharField(
        max_length=100, verbose_name="ФИО сотрудника"
    )
    position = models.CharField(
        max_length=100, verbose_name="Должность сотрудника"
    )
    department = models.CharField(
        max_length=100, verbose_name="Отдел сотрудника", **NULLABLE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
