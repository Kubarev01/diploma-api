

from django.db import models
from apps.common.models import IsDeletedModel
from autoslug import  AutoSlugField
from apps.locations.models import Location
# Create your models here.

# models.py


class Brand(IsDeletedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(unique=True,always_update=False,
                         populate_from="get_slug_source")
    logo = models.FileField(upload_to="brands_images/logo/",null=True,default='brands_images/logo/default.png')
    image = models.FileField(upload_to="brands_images/images",default="brands_images/default.jpg")
    picture = models.ImageField(upload_to="brands_images/pictures",null=True,default="brands_images/pictures/default.png")
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_slug_source(self):
        return f"{self.name}".lower()


class TariffPlan(IsDeletedModel):
    name = models.CharField(max_length=100, verbose_name="Название тарифа")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена в день")
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Скидка (%)")
    active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return f"{self.name} - {self.price_per_day}₽"






BODY_TYPES=(
    ("седан","седан"),
    ("купе","купе"),
    ("хетчбэк","хетчбэк"),
    ("кроссовер","кроссовер"),
    ("джип","джип")
)


class Car(IsDeletedModel):
    model = models.CharField(max_length=150,verbose_name="модель")

    brand = models.ForeignKey(to=Brand, null=True, blank=True, on_delete=models.SET_NULL)
    year_released = models.IntegerField(verbose_name="год выпуска")
    description = models.TextField(verbose_name="описание",max_length=2000,blank=True,null=True)
    slug = AutoSlugField(unique=True,always_update=False,default='',
                         populate_from="get_slug_source")
    engine_volume =models.DecimalField(decimal_places=1,max_digits=2,verbose_name="объем двигателя")
    color = models.CharField(max_length=50,verbose_name="Цвет кузова")
    current_location = models.ForeignKey(to=Location,verbose_name="локация",on_delete=models.CASCADE,blank=True,null=True)
    body_type = models.CharField(choices=BODY_TYPES,default='седан',null=True,blank=True,verbose_name="кузов")
    state_number = models.CharField(max_length=9,verbose_name="гос номер",null=True,blank=True,unique=True)
    tariff_plan = models.ForeignKey(to=TariffPlan,verbose_name="тарифный план",null=True,blank=True,on_delete=models.SET_NULL)
    available = models.BooleanField(verbose_name="доступна для аренды",default=True)

    image1 = models.ImageField(upload_to="car_images/",default="car_images/default.jpg")
    image2 = models.ImageField(upload_to="car_images/",blank=True)
    image3 = models.ImageField(upload_to="car_images/",blank=True)

    class Meta:
        ordering =["-id"]
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.brand} {self.model} | {self.state_number}"

    def get_slug_source(self):
        return f"{self.brand}-{self.model}-{str(self.id)[:8] or ''}"







