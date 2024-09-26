from datetime import datetime, timezone
from rest_framework.serializers import ValidationError


def validate_deadline(value):
    """ Валидация: нельзя указывать прошедшую дату дедлайна. """
    dt_now = datetime.now(timezone.utc)

    if value < dt_now:
        raise ValidationError(
            f"Указанный дедлайн {value.strftime('%d.%m.%Y %H:%M')} невозможен! "
            f"Сегодня {dt_now.strftime('%d.%m.%Y %H:%M')}!"
        )


class StatusValidator:
    """ Валидация: нельзя назначать сотрудника на просроченную заявку. """
    def __init__(self, field_emp, field_status):
        self.field_emp = field_emp
        self.field_status = field_status

    def __call__(self, value):
        tmp_val_emp = dict(value).get(self.field_emp)
        tmp_val_status = dict(value).get(self.field_status)
        if tmp_val_status == 'overdue':
            if tmp_val_emp:
                raise ValidationError(
                    "Нельзя назначать сотрудника на заявку со статусом 'Просрочена'!"
                )
