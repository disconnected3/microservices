from http.client import USE_PROXY
from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import permissions


class RetrieveUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        
        
        return Response({
            "id":request.user.id,
            "username":request.user.username,

        })