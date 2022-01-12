from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from .serializers import ChatingRoomSerializer, MessageCreateSerializer, ChatingRoomMessageListSerializer

from ..models import ChatingRoomMessage, ChatingRoom
from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404

User = get_user_model()


class RoomListAPIView(ListAPIView):
    serializer_class = ChatingRoomSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = None

    def get_chating_room_qs(self):
        user = self.request.user
        qs = ChatingRoom.objects.none()
        qs |= user.user1_chating_room.all()
        qs |= user.user2_chating_room.all()
        return qs

    def get_user_values(self):
        qs = self.get_chating_room_qs()
        lst = []
        for i in range(1, 2):
            new_qs = qs.values_list(f"user{i}", flat=True).distinct()
            if new_qs.exists():
                lst.append(new_qs[0])
        try:
            lst.remove(self.request.user.id)
        except ValueError:
            pass

        return lst

    # def get_queryset(self):
    #     user_values = self.get_user_values()
    #     qs = User.objects.none()
    #     for i in user_values:
    #         qs |= User.objects.filter(id=i)

    #     return qs

    def get_queryset(self):
        qs = self.get_chating_room_qs()
        return qs


class MessageCreateAPIVIew(CreateAPIView):
    serializer_class = MessageCreateSerializer
    lookup_url_kwarg = "username"

    def get_user(self):
        user = self.kwargs.get(self.lookup_url_kwarg)
        if user == self.request.user.username:
            raise ValidationError("Both user cannot be the same")
        return get_object_or_404(User, username=user)

    def perform_create(self, serializer):
        user2 = self.get_user()
        curr_user = self.request.user

        if curr_user == user2:
            raise PermissionDenied("User cannot send itself message")

        room = ChatingRoom.objects.get_or_create_room(curr_user.username, user2.username)

        serializer.save(user1=curr_user, user2=user2, sent_by_user=curr_user, chat_room=room)


class RoomMessagesListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChatingRoomMessageListSerializer
    lookup_url_kwarg = "username"

    def get_user_by_username(self):
        username = self.kwargs.get(self.lookup_url_kwarg)
        user = get_object_or_404(User, username=username)
        if self.request.user == user:
            raise PermissionDenied("Room with own-self is defined...")

        return user

    def get_queryset(self):
        get_user = self.get_user_by_username()
        obj = ChatingRoom.objects.get_or_create_room(get_user.username, self.request.user.username)
        qs = obj.ch_messages.all()

        return qs



