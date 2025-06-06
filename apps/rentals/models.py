from django.db import models
from apps.common.models import IsDeletedModel
from django.db.models import ForeignKey
from apps.cars.models import Car
from apps.users.models import User
from apps.locations.models import Location


STATUS_CHOICES = [
    ('pending', 'Ожидает подтверждения'),
    ('confirmed', 'Подтверждён'),
    ('active', 'Активна'),
    ('completed', 'Завершена'),
    ('cancelled', 'Отменена пользователем'),
    ('rejected', 'Отклонена админом'),
]

class Rentals(IsDeletedModel):
    car = ForeignKey(to=Car,on_delete=models.CASCADE)
    user = ForeignKey(to=User,on_delete=models.CASCADE)
    location_from = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name="bookings_start")
    location_to = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name="bookings_end")
    date_from = models.DateField()
    date_to = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.car.brand} {self.car.model} rented by {self.user}"