from django.contrib import admin
from .models import Car, Brand, TariffPlan

# Register your models here.

admin.site.register(Car)
admin.site.register(Brand)
admin.site.register(TariffPlan)