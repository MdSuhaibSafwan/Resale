from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from .serializers import ChatingRoomSerializer, MessageCreateSerializer, ChatingRoomMessageListSerializer, OfferSerializer

from django.db.models import Q
from ..models import ChatingRoomMessage, ChatingRoom, Offer
from django.contrib.auth import get_user_model
from products.models import Product

from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated

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


class OfferListCreateAPIView(ListCreateAPIView):
    lookup_url_kwarg = "username"
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated, ]

    def get_user(self):
        username = self.kwargs.get(self.lookup_url_kwarg)
        if username == self.request.user.username:
            raise PermissionDenied("Offer with ownself is denied")
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise NotFound("User with this username not found.")

        return user

    def get_offers(self):
        user = self.get_user()
        curr_user = self.request.user
        qs = Offer.objects.filter(Q(from_user=user, to_user=curr_user) | Q(from_user=curr_user, to_user=user))
        return qs
    
    def get_queryset(self):
        qs = self.get_offers()
        return qs.filter(disabled=False)

    def get_counter_offer(self, qs=None):
        offer_id = self.request.query_params.get("offer_id")
        if offer_id is None:
            if qs is None:
                raise PermissionDenied("Internal server error")
            
            qs = qs.filter(disabled=False, to_user=self.request.user)
            if qs.exists():
                raise PermissionDenied("Pls provide a Offer id for counter offer")

        try:
            offer = Offer.objects.get(id=offer_id)
        except ObjectDoesNotExist:
            raise NotFound("Offer with this id is not found.")

        curr_user = self.request.user
        if offer.disabled == True:
            raise PermissionDenied("Offer is Disabled")

        if offer.from_user == curr_user:
            raise PermissionDenied("Own offer cannot be given a counter offer")

        return offer   

    def perform_create(self, serializer):
        qs = self.get_offers()
        print(qs)
        if qs.filter(accepted=True).exists():
            raise PermissionDenied("An offer has been accepted")
        user = self.get_user()
        curr_user = self.request.user
        product = self.get_product()
        counter_offer = self.get_counter_offer(qs)
        from_user_offer_qs = qs.filter(from_user=curr_user)
        for i in from_user_offer_qs:
            i.disabled = True
            i.save()

        serializer.save(from_user=curr_user, to_user=user, product=product, counter_offer=counter_offer)

    def get_product(self):
        product_id = self.request.query_params.get("product_id")
        if product_id is None:
            raise PermissionDenied("pls provide a product id")

        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            raise NotFound("User with this username not found.")

        return product
