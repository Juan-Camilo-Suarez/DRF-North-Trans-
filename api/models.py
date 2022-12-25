from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models


# Create your models here.


class BaseModel(models.Model):
    # auto_now_add=True sirve para que se crea automatico cuando se cree un modelo
    create_at = models.DateTimeField(auto_now_add=True)
    # se actualiza con la fecha del momento de la actualizacion
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        # para que no se agrege este modelo a la base de datos
        abstract = True


class UserManager(DjangoUserManager):
    def create_user(self, username, password=None, **extra_fields):
        # en vez de username se usa email
        user = self.model(email=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        user = self.model(email=email, is_staff=True, is_superuser=True)
        user.set_password(password)
        user.save()
        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    # de esta manera se puede decir que atributo va hacer de username
    USERNAME_FIELD = "email"
    email = models.EmailField(unique=True, verbose_name="Email")
    password = models.CharField(max_length=200, verbose_name="password")
    # regula quien puede ir al admin
    is_staff = models.BooleanField(default=False, verbose_name="is worker")

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


class ApplicationRegister(models.Model):
    class TypeUser(models.TextChoices):
        client = "client", "client"
        driver = "driver", "driver"

    name = models.CharField(max_length=120, blank=False, verbose_name="Name")
    city = models.CharField(max_length=120, blank=False, verbose_name="City")
    email = models.EmailField(max_length=120, blank=False, verbose_name="Email")
    phone = models.CharField(max_length=120, blank=False, verbose_name="Phone")
    user_position = models.CharField(
        max_length=15,
        choices=TypeUser.choices,
        verbose_name="Type User",
    )

    class Meta:
        verbose_name = "Application Register"
        verbose_name_plural = "Applications Register"
