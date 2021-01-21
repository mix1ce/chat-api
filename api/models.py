from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone

from users.models import CustomUser


# Table with a list of chat groups
class Chat(models.Model):

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        CustomUser, related_name='chats', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Table with a list of chat participants
class Party(models.Model):

    chat = models.ForeignKey(
        Chat, related_name='parties', on_delete=models.CASCADE)
    user = models.ForeignKey(
        CustomUser, related_name='parties', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Party')
        verbose_name_plural = _('Parties')
        unique_together = (('user', 'chat'), )

    def __str__(self):
        return f'User: {self.user.email} was added in chat: {self.chat.name}'


# Table with a list of messages
class Message(models.Model):

    chat = models.ForeignKey(
        Chat, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(
        CustomUser, related_name='messages', on_delete=models.CASCADE)
    content = models.CharField(max_length=1023)
    date_created = models.DateTimeField(
        _('date created'), default=timezone.now)

    class Meta:
        index_together = (('user', 'chat'), )

    def __str__(self):
        return self.content


# Table with message statuses
class MessageStatus(models.Model):

    message = models.ForeignKey(
        Message, related_name='message_status', on_delete=models.CASCADE)
    user = models.ForeignKey(
        CustomUser, related_name='message_status', on_delete=models.CASCADE)
    is_read = models.BooleanField(_('read'), default=False)

    class Meta:
        verbose_name = _('Message status')
        verbose_name_plural = _('Message statuses')
        index_together = (('user', 'message'), )

    def __str__(self):
        return f'{self.is_read}'

    def get_absolute_url(self):
        return "/api_message_status"
