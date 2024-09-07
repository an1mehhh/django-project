# mailing/tasks.py
from celery import shared_task
from django.core.mail import send_mail

from config import settings
from .models import Mailing
from message.models import Message


@shared_task
def schedule_mailing(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)
    message = Message.objects.get(mailing=mailing)

    for recipient in mailing.recipients.split(','):
        send_mail(
            subject=message.subject,
            message=message.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient],
            fail_silently=False,
        )

    # Обновляем статус рассылки на завершенный
    mailing.status = 'completed'
    mailing.save()

