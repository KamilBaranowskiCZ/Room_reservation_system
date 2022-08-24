from urllib import response
from django.test import TestCase, Client
from django.urls import reverse
from Reservations.models import ConferenceRoom, Reservation


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.room_list_url = reverse("room-list")
        self.add_room_url = reverse("add-room")
        self.delete_room_url = reverse("delete-room", args=[1])
        self.edit_room_url = reverse("edit-room", args=[1])
        self.reserve_room_url = reverse("reserve-room", args=[1])
        self.room_details_url = reverse("room-details", args=[1])
        self.room_search_url = reverse("room-search")

    @classmethod
    def setUpTestData(cls):
        cls.room1 = ConferenceRoom.objects.create(
            name="mojtest", capacity=1000, has_projector=True
        )

    def test_rooms_list_GET(self):
        response = self.client.get(self.room_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "rooms_list.html")

    def test_add_room_GET(self):
        response = self.client.get(self.add_room_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "add_conference_room.html")

    def test_add_room_POST(self):
        response = self.client.post(
            self.add_room_url,
            {"room_name": "test2", "capacity": 1000, "projector": True},
        )
        room1 = ConferenceRoom.objects.get(id=2)
        self.assertEquals(room1.name, "test2")

    def test_delete_room_GET(self):
        rooms = ConferenceRoom.objects.count()
        self.assertEquals(rooms, 1)
        response = self.client.get(self.delete_room_url)

        rooms = ConferenceRoom.objects.count()

        self.assertEquals(response.status_code, 302)
        self.assertEquals(rooms, 0)

    def test_edit_room_GET(self):
        response = self.client.get(self.edit_room_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_room.html")

    def test_edit_room_POST(self):
        response = self.client.post(
            self.edit_room_url,
            {
                "room_name": "test3",
                "capacity": 5000,
                "projector": False,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.room1.refresh_from_db()
        self.assertEquals(self.room1.name, "test3")

    def test_reserve_room_GET(self):
        response = self.client.get(self.reserve_room_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "reservation.html")

    def test_reserve_room_POST(self):
        response = self.client.post(
            self.reserve_room_url,
            {"room_id": 1, "reservation-date": "2022-08-27", "comment": "testComment"},
        )
        reservation1 = Reservation.objects.get(id=1)
        self.assertEquals(reservation1.comment, "testComment")

    def test_room_details_GET(self):
        response = self.client.get(self.room_details_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "room_details.html")

    def test_room_search_GET(self):
        room1 = ConferenceRoom.objects.get(id=1)
        response = self.client.get(self.room_search_url, {"capacity": 900})
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(
            ConferenceRoom.objects.filter(name__icontains="test"), [room1]
        )
        self.assertTemplateUsed(response, "rooms_list.html")
