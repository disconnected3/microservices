from django.db import models
from django.contrib.auth.models import User
import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Friend(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="chat_user")
    friend  = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="chat_friend")

    def __str__(self):
        return f"{self.user.user.username} -> {self.friend.user.username}"
    

class Room(models.Model):
    friends = models.ForeignKey(Friend,on_delete=models.CASCADE)
    uid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )


    def __str__(self):
        return str(uuid)


class Chat(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="chat_user_related",null=True)
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name="chat_room_related",null=True)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:10]


@receiver(post_save, sender=User, dispatch_uid="auto_user_profile")
def create_profile(sender, instance,created, **kwargs):
    if created:
        profile = UserProfile.objects.create(
            user=instance
        )
        profile.save()