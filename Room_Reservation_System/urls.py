"""Room_Reservation_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Reservations.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RoomListView.as_view(), name="room-list"),
    path("room/new/", AddRoomView.as_view(), name="add-room"),
    path(
        "room/delete/<int:room_id>/",
        DeleteRoomView.as_view(),
        name="delete-room",
    ),
    path("room/edit/<int:room_id>/", EditRoomView.as_view(), name="edit-room"),
    path(
        "room/reserve/<int:room_id>/",
        RoomReservationView.as_view(),
        name="reserve-room",
    ),
    path("room/<int:room_id>/", RoomDetailsView.as_view(), name="room-details"),
    path("search/", SearchView.as_view(), name="room-search"),
]
