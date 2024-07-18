from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators

from .constants import (MAX_LENGTH, ADMIN,
                        EMAIL_LEHGTH, ROLES, USER, MODERATOR)


class User(AbstractUser):

    username = models.CharField(
        validators=[validators.RegexValidator(regex=r'^[\w.@+\- ]+$'), ],
        max_length=MAX_LENGTH,
        unique=True,
        blank=False,
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=EMAIL_LEHGTH,
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=MAX_LENGTH,
        choices=ROLES,
        default=USER,
    )
    first_name = models.CharField(
        'Имя',
        max_length=MAX_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=MAX_LENGTH,
        blank=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=MAX_LENGTH,
        null=True
    )

    @property
    def is_admin(self):
        return (
            self.role == ADMIN
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return (
            self.role == MODERATOR
            or self.is_superuser
        )

    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
