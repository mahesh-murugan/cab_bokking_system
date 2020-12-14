from django.contrib import admin
from booking_app.models import Bookings, Drivers, Profile
# Register your models here.

admin.site.register(Bookings)
admin.site.register(Drivers)
admin.site.register(Profile)
