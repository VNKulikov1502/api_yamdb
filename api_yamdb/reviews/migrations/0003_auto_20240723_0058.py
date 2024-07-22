# Generated by Django 3.2 on 2024-07-22 19:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_alter_review_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Score must be at least 1.'), django.core.validators.MaxValueValidator(10, message='Score must be at most 10.')]),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='unique_review'),
        ),
    ]
