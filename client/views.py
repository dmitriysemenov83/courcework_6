from random import sample

from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin

from blogpost.models import Blogpost
from client.forms import ClientForm, MailingForm, MessageForm
from client.models import Client, Mailing, Message, MailingLog


def main_page(request):
    # Получаем данные из базы данных
    num_mailings = Mailing.objects.count()
    num_active_mailings = Mailing.objects.filter(status='started').count()
    num_unique_clients = Client.objects.filter(mailing__isnull=False).distinct().count()
    random_articles = sample(list(Blogpost.objects.filter(is_published=True)), 3)
    # Выводим шаблон с полученными данными
    return render(request, 'client/main_page.html', {
        'num_mailings': num_mailings,
        'num_active_mailings': num_active_mailings,
        'num_unique_clients': num_unique_clients,
        'random_articles': random_articles,
        'title': 'Главная страница'
    })


def logs(request):
    context = {
        'object_list': MailingLog.objects.all(),
        'title': 'Логи'
    }
    return render(request, 'logs.html', context)


class HomeView(ListView):
    model = Client
    template_name = 'Client/home.html'
    extra_context = {
        'title': 'Клиенты'
    }


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    # fields = ('fullname', 'email', 'comment',)
    success_url = reverse_lazy ('client:home')


class ClientDetailView(DetailView):
    model = Client
    template_name = 'client/detail.html'


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:home')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client:home')


class MailingListView(ListView):
    model = Mailing
    fields = ('time', 'period', 'status', 'clients')
    extra_context = {
        'title': 'Рассылки'
    }
    success_url = reverse_lazy('mailing:list')


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = MailingForm
    success_url = reverse_lazy('client:mailing_list')


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'client/mailing_detail.html'


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('client:mailing_list')


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('client:mailing_list')


class MessageListView(ListView):
    model = Message
    fields = ('title', 'content')
    extra_context = {
        'title': 'Сообщения'
    }
    success_url = reverse_lazy('message:list')


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('client:message_list')


class MessageDetailView(DetailView):
    model = Message
    template_name = 'client/message_detail.html'


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('client:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('client:message_list')
