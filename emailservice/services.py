import smtplib
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.cache import cache
from django.core.mail import send_mail

from config import settings
from config.settings import CACHE_ENABLED
from emailservice.models import Mailing, Log


# Функция старта периодических задач
def start():
    scheduler = BackgroundScheduler()
    if not scheduler.get_jobs():
        scheduler.add_job(send_mailing, 'interval', seconds=50)
    if not scheduler.running:
        scheduler.start()


# Главная функция по отправке рассылки
def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = Mailing.objects.filter(status_mail__in=[Mailing.START, Mailing.CREATE])

    for mailing in mailings:
        # Если достигли end_date, завершить рассылку
        if mailing.stop_mail and current_datetime >= mailing.stop_mail:
            mailing.status_mail = Mailing.STOP
            mailing.save()
            continue  # Пропустить отправку, если end_date достигнут

        # Проверить, нужно ли отправить сообщение в текущий момент времени
        if mailing.next_send_time and current_datetime >= mailing.next_send_time:
            mailing.status_mail = Mailing.START
            clients = mailing.clients.all()
            try:
                server_response = send_mail(
                    subject=mailing.name,
                    message=mailing.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in clients],
                    fail_silently=False,
                )
                Log.objects.create(status=Log.SUCCESS,
                                   server_response=server_response,
                                   mailing=mailing, )
                mailing.last_send_at = current_datetime
            except smtplib.SMTPException as e:
                Log.objects.create(status=Log.FAIL,
                                   server_response=str(e),
                                   mailing=mailing, )

            # Обновление времени следующей отправки
            if mailing.period_mail == Mailing.DAY:
                mailing.next_send_time += timedelta(days=1)
            elif mailing.period_mail == Mailing.WEEK:
                mailing.next_send_time += timedelta(weeks=1)
            elif mailing.period_mail == Mailing.MONTH:
                mailing.next_send_time += timedelta(days=30)

            mailing.save()


def get_messages_from_cache():
    """
    Получение списка сообщений из кэша. Если кэш пуст,то получение из БД.
    """
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    else:
        key = 'categories_list'
        messages = cache.get(key)
        if messages is not None:
            return messages
        else:
            messages = Mailing.objects.all()
            cache.set(key, messages)
            return messages


def get_mailings_from_cache():
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    key = 'mailings_list'
    mailings = cache.get(key)
    if not mailings:
        mailings = Mailing.objects.all()
        cache.set(key, mailings)
        return mailings
    return mailings
