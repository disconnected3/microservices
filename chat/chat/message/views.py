from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chat, Friend, Room, UserProfile
from .serializers import ChatSerializer
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

def index(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse("Authentication Required!")
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return HttpResponse("User Doesnt have a Profile. Please create one.")
    friends = Friend.objects.filter(Q(user=user_profile) | Q(friend=user_profile))
    return render(request,"chat/index.html",{"friends":friends})

@csrf_exempt
def get_or_create_room(request,friend_id):
    try:
        friendship = Friend.objects.get(id=friend_id)
    except Friend.DoesNotExist:
        return JsonResponse({"message":"User Doesn't have a Profile. Please create one!","status":400})
    
    try:
        room = Room.objects.get(friends=friendship)
    except Room.DoesNotExist:
        room = Room.objects.create(
            friends=friendship
        )
        room.save()
    
    return JsonResponse({"room_id":str(room.uid),"status":200})

def room(request, room_id):

    return render(request, 'chat/room.html', {
        'room_id': room_id
    })


class ListMessages(APIView):

    def get(self,request,*args,**kwargs):

        room_id = kwargs.get("room_id")

        if not room_id:
            return Response({"message":"Invalid Room ID"},status=status.HTTP_400_BAD_REQUEST)
        
        messages = Chat.objects.filter(room_id=room_id)

        serializer = ChatSerializer(messages,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)



