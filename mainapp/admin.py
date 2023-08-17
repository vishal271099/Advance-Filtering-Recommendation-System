from django.contrib import admin
from .models import UserRegistration, ListingModel,ContactModel,BookingModel

admin.site.register(UserRegistration)
admin.site.register([ListingModel,ContactModel,BookingModel])
