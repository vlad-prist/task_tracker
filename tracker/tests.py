from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from tracker.models import Employee, Task


class EmployeeTestCase(APITestCase):
    """ Тест экземпляра модели Employee. """
    def setUp(self):
        """ Создание экземпляра модели Employee для дальнейших тестов. """
        self.employee = Employee.objects.create(
            name='Иван Иванов',
            position='Разработчик',
            department='IT'
        )

    def test_employee_retrieve(self):
        """ Тест на получение сотрудника по ПК. """
        url = reverse("tracker:employee-detail", args=(self.employee.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data['name'], self.employee.name
        )

    def test_employee_create(self):
        """ Тест на создание нового экземпляра модели Employee. """
        url = reverse("tracker:employee-list")
        data = {
            'name': 'Петр Петров',
            'position': 'Менеджер HR',
            'department': 'HR'
        }
        response = self.client.post(url, data=data)
        # print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Employee.objects.all().count(), 2
        )

    def test_employee_update(self):
        """ Тест на обновление экземпляра модели Employee. """
        url = reverse('tracker:employee-detail', args=(self.employee.pk,))
        data = {
            'name': 'Иван Иванович',
            'position': 'Разработчик Python',
            'department': 'IT'
        }
        response = self.client.get(url, data=data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('position'), self.employee.position
        )

    def test_employee_delete(self):
        """ Тест удаления экземпляра модели Employee. """
        url = reverse('tracker:employee-detail', args=(self.employee.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Employee.objects.all().count(), 0
        )

    def test_employee_list(self):
        """ Тест вывод списка всех экземпляров модели Employee. """
        url = reverse('tracker:employee-list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            len(data['results']), Employee.objects.all().count()
        )


class TaskTestCase(APITestCase):
    """ Тест экземпляра модели Task. """

    def setUp(self):
        self.task_one = Task.objects.create(
            title="Task one",
            description="This is a test task",
            deadline=timezone.now() + timedelta(days=1),
            status=Task.STATUS_CREATED,
        )
        self.employee = Employee.objects.create(
            name='Иван Иванов',
            position='Разработчик',
            department='IT'
        )

    def test_task_retrieve(self):
        """ Тест на получение задачи по ПК. """
        url = reverse("tracker:task-detail", args=(self.task_one.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data['title'], self.task_one.title
        )

    def test_task_create(self):
        """ Тест на создание новой задачи. """
        url = reverse("tracker:task-list")
        deadline = timezone.now() + timedelta(days=1)
        data = {
            'title': 'Task two',
            'description': 'This is another test task',
            'deadline': deadline.strftime('%d.%m.%Y %H:%M'),
            'employee': self.employee.pk,
            'status': Task.STATUS_IN_PROGRESS,
            'priority': 'high',
        }
        response = self.client.post(url, data=data)
        # print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Task.objects.all().count(), 2
        )

    def test_task_update(self):
        """  Тест на обновление задачи. """
        url = reverse('tracker:task-detail', args=(self.task_one.pk,))
        deadline = timezone.now() + timedelta(days=1)
        data = {
            'title': "Task one updated",
            'description': 'This is a test task',
            'deadline': deadline.strftime('%d.%m.%Y %H:%M'),
            'employee': self.employee.pk,
            'priority': 'medium',
            'status': Task.STATUS_IN_PROGRESS,
        }
        response = self.client.put(url, data=data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Task.objects.get(pk=self.task_one.pk).priority, 'medium'
        )

    def test_task_partial_update(self):
        """ Тест на частичное обновление задачи. """
        url = reverse('tracker:task-detail', args=(self.task_one.pk,))
        data = {
            'title': 'Task one partial updated',
        }
        response = self.client.patch(url, data=data)
        # print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Task.objects.get(
                pk=self.task_one.pk
            ).title, 'Task one partial updated'
        )

    def test_task_delete(self):
        """ Тест на удаление задачи. """
        url = reverse('tracker:task-detail', args=(self.task_one.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(
            Task.objects.all().count(), 0
        )

    def test_task_list(self):
        """ Тест вывод списка всех экземпляров модели Task. """
        url = reverse('tracker:task-list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            len(data['results']), Task.objects.all().count()
        )

    def test_change_status(self):
        """ Тест на изменение статуса задачи при назначении сотрудника. """
        url = reverse('tracker:task-detail', args=(self.task_one.pk,))
        data = {
            'employee': self.employee.pk,
        }
        response = self.client.patch(url, data=data)
        # print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Task.objects.get(
                pk=self.task_one.pk
            ).status, Task.STATUS_IN_PROGRESS
        )

    def test_validation_deadline(self):
        """ Тест валидации дедлайна. """
        url = reverse("tracker:task-list")
        deadline = timezone.now() - timedelta(days=1)
        data = {
            'title': 'Task three',
            'description': 'This is yet another test task',
            'deadline': deadline.strftime('%d.%m.%Y %H:%M'),
            'employee': self.employee.pk,
            'status': Task.STATUS_IN_PROGRESS,
            'priority': 'high',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
        # self.assertEqual(
        #     response.json()['deadline'][0], f'{validate_deadline(deadline)}'
        # )

    def test_overdue_task(self):
        """ Тест на проверку просроченной задачи. """
        url = reverse('tracker:task-list')
        deadline = timezone.now() + timedelta(days=1)
        data = {
            'title': 'Task four',
            'description': 'This is another test task with overdue status',
            'deadline': deadline.strftime('%d.%m.%Y %H:%M'),
            'employee': self.employee.pk,
            'status': Task.STATUS_OVERDUE,
            'priority': 'high',
        }
        response = self.client.post(url, data=data)
        # print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
