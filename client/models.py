from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='Email')
    fullname = models.CharField(max_length=255, verbose_name='ФИО')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    def __str__(self):
        return f'{self.fullname} {self.comment} {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Контент')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    def __str__(self):
        return f'{self.title} {self.content}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    TIME_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )
    STATUS_CHOICES = (
        ('completed', 'Завершена'),
        ('created', 'Создана'),
        ('started', 'Запущена'),
    )
    period = models.CharField(max_length=10, choices=TIME_CHOICES, verbose_name='Период')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус')
    time = models.TimeField(verbose_name='Время')
    next_run = models.DateField()
    message = models.ForeignKey(Message, on_delete=models.CASCADE, default=1)
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    def __str__(self):
        return f'{self.time} {self.period} {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLog(models.Model):
    date_time = models.DateTimeField(verbose_name='Дата и время')
    status = models.CharField(max_length=10, verbose_name='Статус')
    server_response = models.TextField(**NULLABLE, verbose_name='Ответ сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    def __str__(self):
        return f'{self.date_time} {self.status} {self.server_response}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
