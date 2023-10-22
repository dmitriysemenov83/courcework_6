from random import sample

from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin

from blogpost.models import Blogpost
from client.forms import ClientForm, MailingForm, MessageForm
from client.models import Client, Mailing, Message, MailingLog


# @cache_page(60)
def main_page(request):
    # Получаем данные из базы данных
    num_mailings = Mailing.objects.count()
    num_active_mailings = Mailing.objects.filter(status='created').count()
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


class LogListView(ListView):
    model = MailingLog
    template_name = 'client/logs.html'
    context_object_name = 'logs'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class HomeView(ListView):
    model = Client
    template_name = 'client/clients.html'
    extra_context = {
        'title': 'Клиенты'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    # fields = ('fullname', 'email', 'comment',)
    success_url = reverse_lazy('client:clients')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientDetailView(DetailView):
    model = Client
    template_name = 'client/detail.html'


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:clients')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client:clients')


class MailingListView(ListView):
    model = Mailing
    fields = ('time', 'period', 'status', 'clients')
    extra_context = {
        'title': 'Рассылки'
    }
    success_url = reverse_lazy('mailing:list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('client:mailing_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'client/mailing_detail.html'


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('client:mailing_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


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

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('client:message_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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
