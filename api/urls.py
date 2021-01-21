from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from api.views import ChatViewSet, MessageViewSet, PartyViewSet
from users.views import CustomUserViewSet


router = routers.DefaultRouter()
router.register('users', CustomUserViewSet)
router.register('chat', ChatViewSet)
router.register('party', PartyViewSet)
router.register('message', MessageViewSet)
# router.register('message-status', MessageStatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
