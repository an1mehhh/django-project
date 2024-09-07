import socket

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from log.models import Log
from mailing.forms import MailingForm
from mailing.models import Mailing
from message.models import Message


def get_server_status(host, port):
    try:
        with socket.create_connection((host, port)) as sock:
            return '200'
    except OSError:
        return '503'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        message_id = self.request.POST.get('message_id')
        if message_id:
            form.instance.message_id = message_id
        else:
            # Устанавливаем значение message_id автоматически
            form.instance.message_id = self.get_default_message_id()

        self.object.save()

        # Устанавливаем значение поля message_id в модели Log
        log = Log(mailing=self.object, message=Message.objects.get(id=self.object.message_id),
                  server_response=self.get_context_data())
        log.message_id = self.object.message_id
        log.server_response = self.response
        log.status = self.object.status
        log.save()

        return redirect('message:create-message')

    def get_default_message_id(self):
        # Логика для получения значения message_id по умолчанию
        # Например, вы можете вернуть ID последнего созданного сообщения
        return Message.objects.latest('id').id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, 'response'):
            host = "127.0.0.1"  # Локальный хост
            port = 8000  # Порт HTTP
            self.response = get_server_status(host, port)  # Сохраняем значение 'response' в экземпляре класса
        context['response'] = self.response
        return context


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_list.html'
    context_object_name = 'mailings'


class MailingDetailView(DetailView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
