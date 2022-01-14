from django.core.exceptions import ObjectDoesNotExist
from .models import ChatingRoomMessage
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .api.serializers import ChatingRoomMessageListSerializer


@receiver(signal=post_save, sender=ChatingRoomMessage)
def websocket_send_message(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        username = instance.get_to_user
        chat_room = f"message_{username}"
        instance_data = json.dumps(ChatingRoomMessageListSerializer(instance).data)
        print("\n")
        print("From Signal", chat_room)

        async_to_sync(channel_layer.group_send)(
            chat_room,
            {
                "type": "send.message",
                "data": instance_data
            }
        )

        print("\n")

