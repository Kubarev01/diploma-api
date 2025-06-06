from autoslug import AutoSlugField
from django.db import models
from apps.common.models import IsDeletedModel


class Location(IsDeletedModel):
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Долгота"
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Широта"
    )
    slug = AutoSlugField(unique=True,populate_from="generate_location_slug",always_update=False,default='')

    def generate_location_slug(self):
        return str(self.pk)[:10]

    def __str__(self):
        return f"{str(self.latitude)[:8]} ; {str(self.longitude)[:8]}"
