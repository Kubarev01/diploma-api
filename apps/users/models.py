from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from apps.common.models import BaseModel, IsDeletedModel
from .managers import CustomUserManager
# Create your models here.



class User(AbstractBaseUser,IsDeletedModel,PermissionsMixin):
    first_name = models.CharField(max_length=50,verbose_name='Имя',null=True)
    last_name = models.CharField(max_length=50,verbose_name="Фамилия",null=True)
    email = models.EmailField(verbose_name="Логин",unique=True)
    avatar = models.CharField(verbose_name='путь к аватару')

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_superuser(self):
        return self.is_staff