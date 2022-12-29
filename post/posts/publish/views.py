from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post,Like
from .serializers import PostSerializer,LikeSerializer


class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]


class LikeView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        post_id = kwargs.get("post_id")
        user = request.user

        user_id = user.id

        if not (user_id and post_id):
            return Response({"message": "User ID and Post ID should be provided!"})
        
        Like.objects.create(
            user_id = user_id,
            post_id=post_id
        ).save()

        num_of_likes = Like.objects.filter(post_id=Post.objects.get(id=int(post_id))).count()

        return Response({"num_of_likes":num_of_likes})
    
    def delete(self,request,*args,**kwargs):
        post_id = kwargs.get("post_id")
        user = request.user

        user_id = user.id

        if not (user_id and post_id):
            return Response({"message":"User ID and Post ID should be provided!"})
        
        Like.objects.get(user_id=user_id,post_id=post_id).delete()

        num_of_likes = Like.objects.filter(post_id=Post.objects.get(id=int(post_id))).count()

        return Response({"num_of_likes":num_of_likes})



