from rest_framework import serializers

from api.models import Chat, Message, MessageStatus, Party


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'name', 'user')

    def create(self, validated_data):
        chat = Chat.objects.create(**validated_data)
        Party.objects.create(user=validated_data['user'], chat=chat)
        return chat


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ('id', 'chat', 'user')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'chat', 'user', 'content', 'date_created')


class MessageStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageStatus
        fields = ('id', 'message', 'user', 'is_read')
