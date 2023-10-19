from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail

from client.models import Mailing
import datetime

from config.settings import EMAIL_HOST_USER


def send_mailing(mailing):
    subject = mailing.message.title
    message = mailing.message.content
    from_email = EMAIL_HOST_USER
    recipient_list = [client.email for client in mailing.clients.all()]
    for recipient in recipient_list:
        send_mail(subject, message, from_email, [recipient])


# def check_mailing():
#     print(f'Время сейчас: {datetime.datetime.now().time()}')
#     print(f'Дата сейчас: {datetime.datetime.now().date()}')
#     now = datetime.datetime.now().time()
#     mailings = Mailing.objects.filter(time__lte=now, next_run__gte=datetime.datetime.now().date())
#     for mailing in mailings:
#         clients = mailing.clients.all()
#         for client in clients:
#             print(client.email)

def check_mailing():
    print(f'Время сейчас: {datetime.datetime.now().time()}')
    print(f'Дата сейчас: {datetime.datetime.now().date()}')
    now = datetime.datetime.now().time()
    mailings = Mailing.objects.filter(time__lte=now, next_run__gte=datetime.datetime.now().date())
    for mailing in mailings:
        send_mailing(mailing)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_mailing, 'interval', minutes=1, id='run_mailing', replace_existing=True, jobstore='default')
    scheduler.start()
