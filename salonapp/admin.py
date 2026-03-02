from django.contrib import admin
from .models import Customer, Service, Appointment

admin.site.register(Customer)
admin.site.register(Service)
admin.site.register(Appointment)
