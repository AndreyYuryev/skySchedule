from django.db import models
from main.utils import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='название курса')
    description = models.TextField(**NULLABLE, verbose_name='описание курса')
    preview = models.ImageField(upload_to='lessons/', verbose_name='превью', **NULLABLE)
    # video_link = models.URLField(verbose_name='ссылка на видео', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='название урока')
    description = models.TextField(**NULLABLE, verbose_name='описание урока')
    preview = models.ImageField(upload_to='lessons/', verbose_name='превью', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    video_link = models.URLField(verbose_name='ссылка на видео', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
