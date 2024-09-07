from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from log.models import Log

from mailing.models import Mailing
from message.forms import MessageForm
from message.models import Message
from mailing.tasks import schedule_mailing
import socket


def get_server_status(host, port):
    try:
        with socket.create_connection((host, port)) as sock:
            return '200'
    except OSError:
        return '503'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        mailing_id = self.request.POST.get('mailing_id')
        if mailing_id:
            form.instance.mailing_id = mailing_id
        else:
            # Устанавливаем значение mailing_id автоматически
            form.instance.mailing_id = self.get_default_mailing_id()

        self.object.save()  # Сохраняем объект модели Message

        schedule_mailing.apply_async(args=[mailing_id])

        # Устанавливаем значение поля message_id в модели Log
        log = Log(mailing=self.object.mailing, message=self.object, server_response=self.get_context_data())
        log.message_id = self.object.id
        log.server_response = self.response
        log.status = 'Отправлено'  # Добавляем статус отправки сообщения
        log.save()  # Сохраняем объект модели Log

        return response

    def get_default_mailing_id(self):
        # Логика для получения значения mailing_id по умолчанию
        # Например, вы можете вернуть ID последней созданной рассылки
        return Mailing.objects.latest('id').id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, 'response'):
            host = "127.0.0.1"  # Локальный хост
            port = 8000  # Порт HTTP
            self.response = get_server_status(host, port)  # Сохраняем значение 'response' в экземпляре класса
        context['response'] = self.response
        return context


class MessageListView(ListView):
    model = Message
    context_object_name = 'messages'


class MessageDetailView(DetailView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message-list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('message:message-list')
