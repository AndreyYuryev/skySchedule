from celery import shared_task
from lms.models import Course, Subscription
from django.core.mail import send_mail
from django.conf import settings


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
