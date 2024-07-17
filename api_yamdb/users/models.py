from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators

from .constants import (MAX_LENGTH, EMAIL_LEHGTH)
from .enums import UserRoles

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
    
    # Здесь нужно использовать группы для роли
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True
    )

    # Используйте метод "is_..." для проверки роли
    def is_user(self):
        return self.groups.filter(name=UserRoles.user.value).exists()
    def is_moderator(self):
        return self.groups.filter(name=UserRoles.moderator.value).exists()
    def is_admin(self):
        return self.groups.filter(name=UserRoles.admin.value).exists()
