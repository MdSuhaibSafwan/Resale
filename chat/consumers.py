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

from .utils import get_user, send_message


class MessageConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print("Connected ", event)
        await self.send({"type": "websocket.accept"})

        url_queries = str(self.scope["query_string"].decode("utf-8"))
        and_split = url_queries.split("&")
        url_queries = {}
        for i in and_split:
            key_pair = i.split("=")
            url_queries[key_pair[0]] = key_pair[1]

        token = url_queries.get("token")

        user = await self.get_user_by_token(token)
        if user is None:
            await self.send({"type": "websocket.close"})
            return False

        print("Authenticated User ->", user)
        self.scope["user"] = user

        chat_room = f"message_{user}"
        print("Chat Room ->", chat_room)

        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name,
        )

    @database_sync_to_async
    def get_user_by_token(self, token):
        qs = Token.objects.filter(key=token)
        if qs.exists():
            return qs.get().user

        return None

    async def send_message(self, event):
        data = event["data"]
        await self.send({"type": "websocket.send", "text": data})

    async def websocket_receive(self, event):
        """
        Data should be something like this comming from Frontend
        {
            "command": "new_message",
            "message": "Hello World",
            "user": "new_user"
        }
        """
        data = json.loads(event["text"])
        print(data, "\n")

        commands = {
            "new_message": self.sned_new_message,
        }

        command = data.get("command")
        try:
            message = data.get("message")
            user = data.get("user")
            await commands[command](message, user)

        except KeyError as e:
            print("KEY ERROR: ", e)
            await self.send({"type": "websocket.close"})

        return False

    async def sned_new_message(self, message, user):
        print("Inside Send Message", message, user)
        user = await get_user(user)
        if user is None:
            await self.send({"type": "websocket.close"})
            return

        print(user)
        curr_user = self.scope["user"]
        message = await send_message(from_user=curr_user, to_user=user, text=message)
        if message is None:
            await self.send({"type": "websocket.close"})
            return

        print(message)
    
    async def websocket_disconnect(self, event):
        print("DISCONNECTED ", event)
