from django.urls import path
from . import views

urlpatterns = [
    path("retrieve-user/",views.RetrieveUser.as_view(),name="retrieve_user"),
]