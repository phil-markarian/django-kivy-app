# Generated by Django 4.2.7 on 2023-12-12 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_remove_task_name_task_created_at_task_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='task',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
