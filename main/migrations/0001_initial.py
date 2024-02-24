# Generated by Django 5.0.2 on 2024-02-23 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='название урока')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание урока')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='lessons/', verbose_name='превью')),
            ],
            options={
                'verbose_name': 'урок',
                'verbose_name_plural': 'уроки',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='название курса')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание курса')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='lessons/', verbose_name='превью')),
                ('video_link', models.CharField(blank=True, max_length=255, null=True, verbose_name='ссылка на видео')),
                ('lessons', models.ManyToManyField(to='main.lesson', verbose_name='уроки')),
            ],
            options={
                'verbose_name': 'курс',
                'verbose_name_plural': 'курсы',
            },
        ),
    ]