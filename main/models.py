from django.db import models

from main.utils import NULLABLE


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='название урока')
    description = models.TextField(**NULLABLE, verbose_name='описание урока')
    preview = models.ImageField(upload_to='lessons/', verbose_name='превью', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='название курса')
    description = models.TextField(**NULLABLE, verbose_name='описание курса')
    preview = models.ImageField(upload_to='lessons/', verbose_name='превью', **NULLABLE)
    video_link = models.CharField(max_length=255, verbose_name='ссылка на видео', **NULLABLE)
    lessons = models.ManyToManyField(Lesson, verbose_name='уроки')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
