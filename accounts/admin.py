from django.contrib import admin
from accounts.models import Customer, ShippingAddress

admin.site.register(Customer)
admin.site.register(ShippingAddress)