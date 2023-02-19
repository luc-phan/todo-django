# Generated by Django 4.1.7 on 2023-02-18 09:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('todo_crud', '0004_todo_created'), ('todo_crud', '0005_alter_todo_created')]

    dependencies = [
        ('todo_crud', '0003_alter_todo_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created'),
        ),
    ]