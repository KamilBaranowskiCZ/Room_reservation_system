from django.contrib import admin

# Register your models here.

from Reservations.models import ConferenceRoom, Reservation

admin.site.register(ConferenceRoom)
admin.site.register(Reservation)
