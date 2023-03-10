from django.urls import path,include
from .views import PostView,LikeView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('post', PostView, basename='post')

urlpatterns = [
    path("c/",include(router.urls)),
    path("like/",LikeView.as_view(),name="like"),
]