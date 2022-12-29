from django.contrib import admin
from .models import Chat, Room,UserProfile,Friend

admin.site.register(Chat)
admin.site.register(UserProfile)
admin.site.register(Friend)
admin.site.register(Room)