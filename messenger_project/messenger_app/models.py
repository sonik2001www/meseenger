from django.utils import timezone

from django.db import models
from django.contrib.auth import get_user_model


class Chat(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    user_1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_1')
    user_2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_2')
    last_message_time = models.DateTimeField(default=timezone.now)
    last_message = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'

    def __str__(self):
        return f"{self.user_1} - {self.user_2}"


class Message(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='chat')
    messages = models.TextField(blank=True, null=True, default='')

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
