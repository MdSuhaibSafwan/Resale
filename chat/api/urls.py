from . import views
from django.urls import path

urlpatterns = [
    path("room/", views.RoomListAPIView.as_view(), ),
    path("room/message-create/<username>/", views.MessageCreateAPIVIew.as_view(), ),
    path("room/message-list/<username>/", views.RoomMessagesListAPIView.as_view(), ),
]
