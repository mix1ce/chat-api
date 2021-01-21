from django.contrib import admin

from .models import Chat, Message, MessageStatus, Party


class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')


class PartyAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user', 'content',
                    'date_created')


class MessageStatusAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'is_read')


admin.site.register(Chat, ChatAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(MessageStatus, MessageStatusAdmin)
