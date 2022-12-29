from rest_framework import authentication
from rest_framework import exceptions
import requests


USER_SERVICE_URL = "http://127.0.0.1:8000/auth/retrieve-user/"


class UserRelatedOperations:
    def __init__(self,request=None) -> None:
        self.request = request
    
    def get_user(self,token):
        headers = {"Authorization": f"{token}"}

        response = requests.post(USER_SERVICE_URL,headers=headers)

        if response.status_code == 401:
            return None

        response = response.json()

        username = response.get("username")
        id = response.get("id")
        
        if not (username and id):
            return None

        user = CustomUserObject(username,id)

        return (user,None)


class CustomUserObject:
    def __init__(self,username,id):
        self.username = username
        self.id = id
        self.is_authenticated = True



class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self,request):
        token = request.META.get("HTTP_AUTHORIZATION",None)
        
        if not token:
            return None
        
        return UserRelatedOperations(request=request).get_user(token)

        
        
