from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from mailing.models import Mailing
from message.forms import MessageForm
from message.models import Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message-list')

    def form_valid(self, form):
        mailing_id = self.request.POST.get('mailing_id')
        if mailing_id:
            form.instance.mailing_id = mailing_id
        else:
            # Устанавливаем значение mailing_id автоматически
            form.instance.mailing_id = self.get_default_mailing_id()

        return super().form_valid(form)

    def get_default_mailing_id(self):
        # Логика для получения значения mailing_id по умолчанию
        # Например, вы можете вернуть ID последней созданной рассылки
        return Mailing.objects.latest('id').id


class MessageListView(ListView):
    model = Message
    context_object_name = 'messages'


class MessageDetailView(DetailView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message-list')
