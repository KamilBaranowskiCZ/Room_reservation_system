from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from .models import ConferenceRoom, Reservation
import datetime
from django.core.paginator import Paginator

# Create your views here.

class RoomListView(View):
    def get(self, request):
        rooms_list = ConferenceRoom.objects.all()
        for room in rooms_list:
            reservation_dates = [
                reservation.date for reservation in room.reservation_set.all()
            ]
            room.reserved = datetime.date.today() in reservation_dates
        p = Paginator(rooms_list, 8)
        page = request.GET.get("page")
        rooms = p.get_page(page)
        return render(
            request,
            "rooms_list.html",
            context={"rooms_list": rooms_list, "rooms": rooms},
        )


class AddRoomView(View):
    def get(self, request):
        return render(request, "add_conference_room.html")

    def post(self, request):
        name = request.POST.get("room_name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get("projector") == "on"
        if not name:
            return render(
                request,
                "add_conference_room.html",
                context={"error": "Podaj nazwę sali"},
            )
        if capacity <= 0:
            return render(
                request,
                "add_conference_room.html",
                context={"error": "Podaj dodatnią pojemność sali"},
            )
        try:
            ConferenceRoom.objects.create(
                name=name, capacity=capacity, has_projector=projector
            )
        except:
            return render(
                request,
                "add_conference_room.html",
                context={"error": "Sala o podanej nazwie już istnieje"},
            )
        return redirect("/")


class DeleteRoomView(View):
    def get(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        room.delete()
        return redirect("room-list")


class EditRoomView(View):
    def get(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        return render(request, "edit_room.html", context={"room": room})

    def post(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        name = request.POST.get("room-name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get("projector") == "on"
        if not name:
            return render(
                request,
                "edit_room.html",
                context={"error": "Podaj nazwę sali"},
            )
        if capacity <= 0:
            return render(
                request,
                "edit_room.html",
                context={"error": "Podaj dodatnią pojemność sali"},
            )
        try:
            room.name = name
            room.capacity = capacity
            room.has_projector = projector
            room.save()
        except:
            return render(
                request,
                "edit_room.html",
                context={"error": "Sala o podanej nazwie już istnieje"},
            )
        return redirect("/")


class RoomReservationView(View):
    def get(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        reservations = room.reservation_set.filter(
            date__gte=str(datetime.date.today())
        ).order_by("date")
        return render(
            request,
            "reservation.html",
            context={"room": room, "reservations": reservations},
        )

    def post(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        date = request.POST.get("reservation-date")
        comment = request.POST.get("comment")

        reservations = room.reservation_set.filter(
            date__gte=str(datetime.date.today())
        ).order_by("date")
        if Reservation.objects.filter(room_id=room_id, date=date):
            return render(
                request,
                "reservation.html",
                context={
                    "room": room,
                    "reservations": reservations,
                    "error": "Sala jest już zarezerwowana!",
                },
            )
        if date < str(datetime.date.today()):
            return render(
                request,
                "reservation.html",
                context={
                    "room": room,
                    "reservations": reservations,
                    "error": "Data jest z przeszłości!",
                },
            )
        Reservation.objects.create(
            room_id_id=room_id, date=date, comment=comment
        )

        return redirect("room-list")


class RoomDetailsView(View):
    def get(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        reservations = room.reservation_set.filter(
            date__gte=str(datetime.date.today())
        ).order_by("date")
        return render(
            request,
            "room_details.html",
            context={"room": room, "reservations": reservations},
        )


class SearchView(View):
    def get(self, request):
        name = request.GET.get("room-name")
        capacity = request.GET.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.GET.get("projector") == "on"
        rooms = ConferenceRoom.objects.all()
        if projector:
            rooms = rooms.filter(has_projector=projector)
        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)
        if name:
            rooms = rooms.filter(name__contains=name)
        for room in rooms:
            reservation_dates = [
                reservation.date for reservation in room.reservation_set.all()
            ]
            room.reserved = datetime.date.today() in reservation_dates
        return render(
            request,
            "rooms_list.html",
            context={"rooms": rooms, "date": datetime.date.today()},
        )
