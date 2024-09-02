from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    name = models.CharField(max_length=35, verbose_name="name")
    last_name = models.CharField(max_length=35, verbose_name="last_name", **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='email')
    comment = models.TextField(verbose_name='comment', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, related_name="client")

    def __str__(self):
        return f" {self.name} {self.email}"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"


class Mailing(models.Model):
    DAY = 'ежедневно'
    WEEK = 'раз в неделю'
    MONTH = 'раз в месяц'
    CREATE = 'создана'
    START = 'запущена'
    STOP = 'завершена'
    CHOICE_PERIOD = [
        (DAY, "Раз в день"),
        (WEEK, "Раз в неделю"),
        (MONTH, "Раз в месяц"),
    ]
    CHOICE_STATUS = [
        (STOP, "Завершена"),
        (CREATE, "Создана"),
        (START, "Запущена"),
    ]

    name = models.CharField(max_length=50, verbose_name="Тема рассылки")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменена")
    clients = models.ManyToManyField(Client, related_name="clients", verbose_name="Клиенты")
    start_mail = models.DateTimeField(default=timezone.now, verbose_name="Начало рассылки")
    stop_mail = models.DateTimeField(default=(timezone.now() + timezone.timedelta(days=1)),
                                     verbose_name="Конец рассылки")
    period_mail = models.CharField(
        max_length=100,
        choices=CHOICE_PERIOD,
        default=DAY,
        verbose_name="Периодичность")
    status_mail = models.CharField(max_length=100, choices=CHOICE_STATUS, default=CREATE, verbose_name="Статус")
    next_send_time = models.DateTimeField(verbose_name='Время следующей отправки', **NULLABLE)
    last_send_at = models.DateTimeField(null=True, verbose_name="Последняя рассылка")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f"{self.name} ({self.last_send_at}) {self.owner}"

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        permissions = [
            ('deactivate_mailing', 'Can deactivate mailing'),
            ('view_all_mailings', 'Can view all mailings'),
        ]


class Log(models.Model):
    SUCCESS = 'Успешно'
    FAIL = 'Неуспешно'
    STATUS_VARIANTS = [
        (SUCCESS, 'Успешно'),
        (FAIL, 'Неуспешно'),
    ]

    time = models.DateTimeField(
        verbose_name="Дата и время попытки отправки", auto_now_add=True
    )
    status = models.CharField(max_length=50, choices=STATUS_VARIANTS, verbose_name='Cтатус рассылки')
    server_response = models.CharField(
        max_length=150, verbose_name="Ответ сервера почтового сервиса", **NULLABLE
    )
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")

    def __str__(self):
        return f"{self.mailing} {self.time} {self.status} {self.server_response}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
