from django.urls import path

from message.apps import MessageConfig
from message.views import MessageCreateView, MessageListView, MessageDetailView, MessageDeleteView

app_name = MessageConfig.name

urlpatterns = [
    path('create-message/', MessageCreateView.as_view(), name='create-message'),
    path('messages/', MessageListView.as_view(), name='message-list'),
    path('messages/<int:pk>/edit/', MessageDetailView.as_view(), name='message_edit'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
]
