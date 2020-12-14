from django.db import models
from django.contrib.auth.models import User


class Drivers(models.Model):
    car_types = (("Hatchback", "Hatchback"), ("Sedan", "Sedan"), ("SUV", "SUV"))
    languages = (("English", "English"), ("Hindi", "Hindi"), ("Kannada", "Kannada"))

    name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=30)
    car_type = models.CharField(choices=car_types, max_length=10)
    car_name = models.CharField(max_length=30)
    languages_known = models.CharField(choices=languages, max_length=30)
    available_city = models.CharField(max_length=30)
    price_per_km = models.IntegerField()

    def __str__(self):
        return "name={} , cabname= {}".format(self.name, self.company_name)


class Bookings(models.Model):
    depart_city = models.CharField(max_length=30)
    destination_city = models.CharField(max_length=30)
    depart_date_time = models.DateTimeField()
    return_date_time = models.DateTimeField(null=True)
    pickup_address = models.TextField(null=True)
    pickup_time = models.TextField(null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    driver = models.ForeignKey(Drivers, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(null=True)

    def __str__(self):
        return "Booking depart city= {} and destination city= {}".format(self.depart_city, self.destination_city)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return "{}".format(self.user.username)

