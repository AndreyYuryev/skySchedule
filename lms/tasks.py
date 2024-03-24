from celery import shared_task
from lms.models import Course, Subscription
from users.models import User
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta, datetime


@shared_task
def inform_by_course_update(pk):
    users = []
    title = ''
    subs = Subscription.objects.all().filter(course_id=pk)
    for sub in subs:
        users.append(sub.user.email)
        if not title:
            title = Course.objects.filter(pk=pk).first().title
    if users:
        send_mail(subject='Изменение учебного материала',
                  message=f'Обновлено содержание курса {title}', from_email=settings.EMAIL_HOST_USER,
                  recipient_list=users, fail_silently=False)


@shared_task
def deactivate_user():
    users = User.objects.filter(is_active=True)
    month_ago = datetime.now().date() - timedelta(days=31)
    for user in users:
        if user.last_login is not None:
            if user.last_login.date() < month_ago:
                user.is_active = False
                user.save()
