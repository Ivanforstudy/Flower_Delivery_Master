from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # можно добавить доп. поля, если нужно
    pass
