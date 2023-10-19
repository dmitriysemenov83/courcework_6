from django.urls import path

from . import views
from .apps import ClientConfig
from .services import start_scheduler
from .views import HomeView, ClientCreateView, ClientDetailView, ClientUpdateView, ClientDeleteView, MailingListView, \
    MailingCreateView, MailingDetailView, MailingUpdateView, MailingDeleteView, MessageListView, MessageCreateView, \
    MessageUpdateView, MessageDetailView, MessageDeleteView

app_name = ClientConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('view/<int:pk>', ClientDetailView.as_view(), name='view'),
    path('update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_view/<int:pk>', MailingDetailView.as_view(), name='mailing_view'),
    path('mailing_update/<int:pk>', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>', MailingDeleteView.as_view(), name='mailing_delete'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_view/<int:pk>', MessageDetailView.as_view(), name='message_view'),
    path('message_update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('main_page/', views.main_page, name='main_page'),
]


# start_scheduler()
