# Generated by Django 5.0.2 on 2024-02-23 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_course_lessons_lesson_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='course',
        ),
    ]