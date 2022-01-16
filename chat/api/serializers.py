from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from ..models import ChatingRoom, ChatingRoomMessage, Offer
from products.api.serializers import ProductListCreateSerializer

User = get_user_model()


class ChatingRoomMessageListSerializer(ModelSerializer):
    sent_by_user = serializers.StringRelatedField(read_only=True)
    to_user = serializers.SerializerMethodField()

    class Meta:
        model = ChatingRoomMessage
        exclude = ["chat_room", "user1", "user2"]

    def get_to_user(self, serializer):
        user_1 = serializer.user1
        user_2 = serializer.user2
        sent_user = serializer.sent_by_user

        if sent_user == user_1:
            return user_2.username

        return user_1.username


class MessageCreateSerializer(ModelSerializer):
    user1 = serializers.StringRelatedField(read_only=True)
    user2 = serializers.StringRelatedField(read_only=True)
    sent_by_user = serializers.StringRelatedField(read_only=True)
    chat_room = serializers.StringRelatedField(read_only=True)
    slug = serializers.StringRelatedField(read_only=True)
    seen = serializers.BooleanField(read_only=True)

    class Meta:
        model = ChatingRoomMessage
        fields = "__all__"


class MessageForRoomSerializer(ModelSerializer):

    class Meta:
        model = ChatingRoomMessage
        fields = ["message", ]


class ChatingRoomSerializer(ModelSerializer):
    """
    This Serializer is created to see the list of users current-user has chatted with
    """
    user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unseen_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatingRoom
        exclude = ["user1", "user2", "date_created", "last_updated"]

    def get_user(self, serializer):
        request = self.context.get("request")
        if not request:
            return None

        return self.get_user_from_serializer_and_request(serializer, request).username

    def get_user_from_serializer_and_request(self, serializer, request):
        curr_user = request.user
        if curr_user == serializer.user1:
            return serializer.user2

        return serializer.user1


    def get_last_message(self, serializer):
        obj = serializer.ch_messages.first()
        if not obj:
            return "no_messages"
        serialized = ChatingRoomMessageListSerializer(obj)
        return serialized.data

    def get_unseen_message(self, serializer):
        request = self.context.get("request")
        if not request:
            return None

        user = self.get_user_from_serializer_and_request(serializer, request)
        qs = serializer.ch_messages.filter(seen=False, sent_by_user=user)
        return qs.count()



class ChattingRoomListSerializer(ModelSerializer):
    # user1 = UserSerializer(read_only=True)
    # user2 = UserSerializer(read_only=True)
    user = serializers.SerializerMethodField(default=None)
    last_msg = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatingRoom
        # fields = "__all__"
        exclude = ["user1", "user2"]

    def get_user(self, serializer):
        request = self.context.get("request")
        if request is None:
            return None

        # user = serializer.user2 if serializer.user1 == request.user else serializer.user1
        # serialized = UserSerializer(user)
        # return serialized.data

    def get_last_msg(self, serializer):
        msg = serializer.ch_messages.order_by("-last_updated").first()
        return ChatingRoomMessageListSerializer(msg).data


class RoomForTotalMessagingSerializer(ModelSerializer):
    """
    This Serializer is created to see the list of users current-user has chatted with
    """
    user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unseen_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatingRoom
        exclude = ["user1", "user2", "date_created", "last_updated"]

    def get_user(self, serializer):
        request = self.context.get("request")
        if not request:
            return None

        return self.get_user_from_serializer_and_request(serializer, request).username

    def get_user_from_serializer_and_request(self, serializer, request):
        curr_user = request.user
        if curr_user == serializer.user1:
            return serializer.user2

        return serializer.user1


    def get_last_message(self, serializer):
        obj = serializer.ch_messages.first()
        if not obj:
            return "no_messages"
        serialized = ChatingRoomMessageListSerializer(obj)
        return serialized.data

    def get_unseen_message(self, serializer):
        request = self.context.get("request")
        if not request:
            return None

        user = self.get_user_from_serializer_and_request(serializer, request)
        qs = serializer.ch_messages.filter(seen=False, sent_by_user=user)
        return qs.count()



class OfferSerializer(ModelSerializer):
    from_user = serializers.StringRelatedField()
    to_user = serializers.StringRelatedField()
    accepted = serializers.BooleanField(read_only=True)
    product = ProductListCreateSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Offer
        fields = "__all__"

