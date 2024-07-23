from django.core.exceptions import ValidationError
from datetime import datetime


def validate_year(value):
    if value > datetime.today().year:
        raise ValidationError(
            ('Год не может быть больше текущего.'),
            params={'value': value},
        )
