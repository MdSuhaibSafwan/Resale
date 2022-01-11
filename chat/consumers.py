import json
import asyncio

from channels.consumer import AsyncConsumer
from .models import ChatingRoom, ChatingRoomMessage
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
import json
from django.db.models import Q


class MessageConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print("Connected ", event)
        await self.send({"type": "websocket.accept"})

        # token = self.scope["url_route"]["kwargs"]["token"]
        # user = await self.get_user_by_token(token)
        # chat_room = f"message_{user.username}"
        # print(chat_room)

        # self.chat_room = chat_room
        # await self.channel_layer.group_add(
        #     chat_room,
        #     self.channel_name,
        # )

    @database_sync_to_async
    def get_user_by_token(self, token):
        qs = Token.objects.filter(key=token)
        if qs.exists():
            return qs.get().user

        raise ObjectDoesNotExist("Token with this key does not exist")

    async def send_message(self, event):
        data = event["data"]
        await self.send({"type": "websocket.send", "text": data})

    async def websocket_receive(self, event):
        print("RECEIVED ", event)
        data = json.loads(event["text"])
        # print(data)
        # print("\n")

        # seen = data.get("seen")
        # if seen:
        #     msg_id = data.get("id")
        #     token = data.get("token")
        #     if (not msg_id) or (not token):
        #         raise PermissionDenied("Message and token is necessary")

        #     await self.handle_message_seen(msg_id, token)

    async def handle_message_seen(self, msg_id, token):
        user = await self.get_user_by_token(token)
        print(user)
        msg = await self.mark_as_seen(msg_id, user)
        if msg:
            chat_room = f"message_{msg.sent_by_user}"
            print(chat_room)
            await self.channel_layer.group_send(
                chat_room,
                {
                    "type": "send_seen",
                    "data": "seen",
                },
            )

            print("Sent seen")

    @database_sync_to_async
    def mark_as_seen(self, msg_id, user):
        qs = ChatingRoomMessage.objects.filter(id=int(msg_id))
        if qs.exists():
            msg = qs.get()
            print("Got message")
            print(msg.get_to_user)
            if msg.get_to_user == user:
                msg.seen = True
                msg.save()
                print("Marked as seen")
                return msg
            return None
        raise ObjectDoesNotExist("message with this id is not Found")

    async def send_seen(self, event):
        print("Sending seen")
        await self.send({"type": "websocket.send", "text": event["data"]})

    async def websocket_disconnect(self, event):
        print("DISCONNECTED ", event)