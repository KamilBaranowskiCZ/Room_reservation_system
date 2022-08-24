from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Reservations.views import (
    RoomListView,
    AddRoomView,
    DeleteRoomView,
    EditRoomView,
    RoomReservationView,
    RoomDetailsView,
    SearchView,
)


class TestUrls(SimpleTestCase):
    def test_room_list_url_resolves(self):
        url = reverse("room-list")
        self.assertEquals(resolve(url).func.view_class, RoomListView)

    def test_add_room_url_resolves(self):
        url = reverse("add-room")
        self.assertEquals(resolve(url).func.view_class, AddRoomView)

    def test_delete_room_url_resolves(self):
        url = reverse("delete-room", args=[1])
        self.assertEquals(resolve(url).func.view_class, DeleteRoomView)

    def test_edit_room_url_resolves(self):
        url = reverse("edit-room", args=[1])
        self.assertEquals(resolve(url).func.view_class, EditRoomView)

    def test_room_reservation_url_resolves(self):
        url = reverse("reserve-room", args=[1])
        self.assertEquals(resolve(url).func.view_class, RoomReservationView)

    def test_room_details_url_resolves(self):
        url = reverse("room-details", args=[1])
        self.assertEquals(resolve(url).func.view_class, RoomDetailsView)

    def test_search_room_url_resolves(self):
        url = reverse("room-search")
        self.assertEquals(resolve(url).func.view_class, SearchView)
