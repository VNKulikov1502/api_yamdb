# Generated by Django 3.2 on 2024-07-21 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='author',
        ),
        migrations.RemoveField(
            model_name='review',
            name='title',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
