from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail

from client.models import Mailing, MailingLog
import datetime
from django.utils import timezone

from config.settings import EMAIL_HOST_USER


def send_mailing(mailing):
    print(f'Отправка письма: {datetime.datetime.now().time()}')
    subject = mailing.message.title
    message = mailing.message.content
    from_email = EMAIL_HOST_USER
    recipient_list = [client.email for client in mailing.clients.all()]
    for recipient in recipient_list:
        response = send_mail(subject, message, from_email, [recipient])
        if response == 1:
            status = 'success'
            server_response = 'Письмо доставлено'
        else:
            status = 'error'
            server_response = 'Message не доставлено'

        # Создаем новый объект журнала рассылки и сохраняем его в базу.
        mailing_log = MailingLog(date_time=timezone.now(), status=status, server_response=server_response,
                                 mailing=mailing, user=mailing.user)
        mailing_log.save()
        # send_mail(subject, message, from_email, [recipient])
        #print(recipient)


def check_mailing():
    now = timezone.now()
    mailings = Mailing.objects.filter(status='created', time__lte=now.time(), next_run__lte=now.date())
    for mailing in mailings:
        send_mailing(mailing)
        mailing.start_mailing()

# def check_mailing():
#     print(f'Время сейчас: {datetime.datetime.now().time()}')
#     print(f'Дата сейчас: {datetime.datetime.now().date()}')
#     now = datetime.datetime.now().time()
#     mailings = Mailing.objects.filter(time__lte=now, next_run__gte=datetime.datetime.now().date())
#     for mailing in mailings:
#         send_mailing(mailing)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_mailing, 'interval', minutes=1, id='run_mailing', replace_existing=True, jobstore='default')
    scheduler.start()


# def check_mailing():
#     print(f'Время сейчас: {datetime.datetime.now().time()}')
#     print(f'Дата сейчас: {datetime.datetime.now().date()}')
#     now = datetime.datetime.now().time()
#     mailings = Mailing.objects.filter(time__lte=now, next_run__gte=datetime.datetime.now().date())
#     for mailing in mailings:
#         clients = mailing.clients.all()
#         for client in clients:
#             print(client.email)
