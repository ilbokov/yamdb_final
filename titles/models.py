from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField('Категория', max_length=30)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.TextField(
        unique=True,
        verbose_name='Название жанра')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        default=name,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name[:50]


class Title(models.Model):
    name = models.CharField(
        max_length=300,
        verbose_name='Название'
    )
    year = models.PositiveSmallIntegerField(
        default=2021,
        verbose_name='Год',
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(date.today().year)
        ],
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категории',
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанры',
        related_name='titles',
    )

    def __str__(self):
        return f"{self.name} ({self.year}г.)"
