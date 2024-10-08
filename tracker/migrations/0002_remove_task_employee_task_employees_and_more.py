# Generated by Django 5.1.1 on 2024-09-19 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='employee',
        ),
        migrations.AddField(
            model_name='task',
            name='employees',
            field=models.ManyToManyField(blank=True, null=True, related_name='tasks', to='tracker.employee', verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(help_text='ДД.ММ.ГГГГ 00:00', verbose_name='Срок выполнения'),
        ),
    ]
