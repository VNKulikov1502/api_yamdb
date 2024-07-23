from django.db import models

from api.constants import MAX_NAME_LENGTH, MAX_SLUG_LENGTH
from posts.validators import validate_year


class Category(models.Model):
    name = models.CharField(
        'Название',
        max_length=MAX_NAME_LENGTH,
        help_text='Название категории'
    )
    slug = models.SlugField(
        max_length=MAX_SLUG_LENGTH,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Название',
        max_length=MAX_NAME_LENGTH,
        help_text='Название жанра'
    )
    slug = models.SlugField(
        max_length=MAX_SLUG_LENGTH,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=MAX_NAME_LENGTH,
        help_text='Название произведения')
    year = models.SmallIntegerField(
        'Год выхода',
        validators=[validate_year],
    )

    description = models.TextField(
        'Описание',
        blank=True,
        null=True,
        help_text='Описание произведения')
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Тайтл'
        verbose_name_plural = 'Тайтлы'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre_title'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='genre_title'
    )

    def __str__(self):
        return f'{self.genre} {self.title}'
