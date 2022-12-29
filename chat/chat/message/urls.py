from django.urls import path
from .views import index,room,ListMessages,get_or_create_room

urlpatterns = [
    path("",index,name="index"),
    path("get-or-create-room/<int:friend_id>/",get_or_create_room,name="get_or_create_room"),
    path("<uuid:room_id>/",room,name="room"),
    path("<uuid:room_id>/get-messages/",ListMessages.as_view(),name="get_room_messages"),
]