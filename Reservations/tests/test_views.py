from urllib import response
from django.test import TestCase, Client
from django.urls import reverse
from Reservations.models import ConferenceRoom, Reservation
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.room_list_url = reverse("room-list")
        self.add_room_url = reverse("add-room")
        self.delete_room_url = reverse("delete-room", args=[2])

    def test_rooms_list_GET(self):
        response = self.client.get(self.room_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "rooms_list.html")

    def test_add_room_GET(self):
        response = self.client.get(self.add_room_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "add_conference_room.html")

    def test_add_room_POST(self):
        url = reverse("add-room")
        response = self.client.post(url, {
            'room_name': "test",
            'capacity': 1000,
            'projector': True
        })
        room1 = ConferenceRoom.objects.get(id=1)
        self.assertEquals(room1.name, "test")

    def test_delete_room_GET(self):
        ConferenceRoom.objects.create(name="test2", capacity=1000, has_projector=True)
        rooms = ConferenceRoom.objects.count()
        self.assertEquals(rooms, 1)

        response = self.client.get(self.delete_room_url)

        rooms = ConferenceRoom.objects.count()
        
        self.assertEquals(response.status_code, 302)
        self.assertEquals(rooms, 0)