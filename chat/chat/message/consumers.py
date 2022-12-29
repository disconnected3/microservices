import json
from channels.generic.websocket import WebsocketConsumer
from .models import Chat
from .serializers import ChatSerializer
from asgiref.sync import async_to_sync
from message.authentication import UserRelatedOperations


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = 'chat_%s' % self.room_id

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_id,
            self.channel_name
        )
        self.accept()
    
    def disconnect(self,close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_id,
            self.channel_name
        )

    def receive(self,text_data):
        text_json = json.loads(text_data)
        message = text_json.get("message")
        token = text_json.get("token")

        user = UserRelatedOperations().get_user(f"Bearer {token}")

        if user is None:
            raise ValueError("Invalid Token")
        
        user = user[0]


        chat_obj = Chat.objects.create(
            text=message,
            user_id=user.id,
            room_id=self.room_id
        )

        chat_obj.save()

        serializer = ChatSerializer(chat_obj)
        

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_id,
            {
                "type":"chat_message",
                **serializer.data
            }
        )
    
    def chat_message(self,event):
        message = event.get("text")
        user_id = event.get("user")
        created = event.get("created")

        self.send(text_data=json.dumps({
            "message":message,
            "user_id":user_id,
            "room_id":str(self.room_id),
            "created":created
        }))



class NotificationConsumer(WebsocketConsumer):
    """ Send notification to users when one of the friends share a post """
    
    def connect(self):
        self.user = self.scope["user"] 
        self.notification_group_id = "notification_%s" % self.user.id

        async_to_sync(self.channel_layer.group_add)(
            self.notification_group_id,
            self.channel_name
        )
        self.accept()
    
    def disconnect(self,close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.notification_group_id,
            self.channel_name
        )
    
    def receive(self,text_data):
        text_json = json.loads(text_data)
        post_id = text_json.get("post_id")


        async_to_sync(self.channel_layer.group_send)(
            self.notification_group_id,
            {
                "type":"post_notification",
                "post_id":post_id
            }
        )
    
    def post_notification(self,event):
        post_id = event.get("post_id")

        self.send(text_data = json.dumps({
            "post_id":post_id,
            "user_id":self.user.id
        }))