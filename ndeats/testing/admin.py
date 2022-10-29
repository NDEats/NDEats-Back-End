from django.contrib import admin
from .models import Person, Order, OldOrder

# Register your models here.
admin.site.register(Person)
admin.site.register(Order)
admin.site.register(OldOrder)
