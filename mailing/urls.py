from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import MailingCreateView, MailingListView, MailingUpdateView

app_name = MailingConfig.name

urlpatterns = [
    path('create-mail/', MailingCreateView.as_view(), name='create-mail'),
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/edit/', MailingUpdateView.as_view(), name='mailing_edit'),
]

