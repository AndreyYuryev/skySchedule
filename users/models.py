from django.db import models
from django.contrib.auth.models import AbstractUser
from lms.utils import NULLABLE, PAYMENT_TYPE
from lms.models import Lesson, Course


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='город', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)
    payment_date = models.DateField(verbose_name='дата оплаты')
    amount = models.DecimalField(decimal_places=2, max_digits=16)
    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPE, default=1, verbose_name='тип платежа')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'Платеж {self.user} от {self.payment_date}'
