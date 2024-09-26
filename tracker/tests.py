from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from tracker.models import Employee, Task


class EmployeeTestCase(APITestCase):
    """ Тест экземпляра модели Employee. """
    def setUp(self):
        """ Создание экземпляра модели Employee для дальнейших тестов. """
        self.employee = Employee.objects.create(name='Иван Иванов', position='Разработчик', department='IT')

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
