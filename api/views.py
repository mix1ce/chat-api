from users.models import CustomUser
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from api.serializers import ChatSerializer, MessageSerializer, MessageStatusSerializer, PartySerializer
from api.models import Chat, Message, MessageStatus, Party


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['POST'])
    def messages(self, request, pk=None):
        if 'index_from' and 'index_to' in request.data:
            data = []
            index_from = request.data['index_from']
            index_to = request.data['index_to']
            user = request.user
            queryset = Message.objects.filter(
                chat=pk).order_by('-id')[index_from:index_to:-1]

            for message in queryset:
                serializer = MessageSerializer(message, many=False)
                message_status = MessageStatus.objects.get(
                    user=user, message=message.id)
                message_status.is_read = True
                message_status.save()
                data.append(serializer.data)

            response = {'message': 'Chat messages',
                        'result': data}
            return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'You need to send index_from and index_to'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def send_message(self, request, pk=None):

        if 'content' in request.data:
            content = request.data['content']
            chat = Chat.objects.get(id=pk)
            user = request.user
            chat_participants = CustomUser.objects.filter(
                parties__in=Party.objects.filter(chat=pk))

            message = Message.objects.create(
                user=user, chat=chat, content=content)

            for participant in chat_participants:
                if participant == user:
                    MessageStatus.objects.create(
                        user=participant, message=message, is_read=True)
                else:
                    MessageStatus.objects.create(
                        user=participant, message=message)

            serializer = MessageSerializer(message, many=False)

            response = {'message': 'Message sent',
                        'result': serializer.data}

            return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'You need to send message'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=['POST'])
    # def add_participant(self, request, pk=None):
    #     if 'user_id' in request.data:
    #         user_id = request.data['user_id']
    #         chat = Chat.objects.get(id=pk)
    #         # user = request.user
    #         user = CustomUser.objects.get(id=user_id)

    #         party = Party.objects.create(chat=chat, user=user)
    #         serializer = MessageSerializer(party, many=False)

    #         response = {'message': 'Message sent',
    #                     'result': serializer.data}

    #         return Response(response, status=status.HTTP_200_OK)

    #     else:
    #         response = {'message': 'You need to send message'}
    #         return Response(response, status=status.HTTP_400_BAD_REQUEST)


class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    http_method_names = ['delete']


# class MessageStatusViewSet(viewsets.ModelViewSet):
#     queryset = Party.objects.all()
#     serializer_class = PartySerializer
#     authentication_classes = (TokenAuthentication, )
#     permission_classes = (IsAuthenticated, )

#     # def update(self, request, *args, **kwargs):
#     #     response = {'message': "You can't update message status like that"}
#     #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

#     def create(self, request, *args, **kwargs):
#         response = {'message': "You can't create message status like that"}
#         return Response(response, status=status.HTTP_400_BAD_REQUEST)
