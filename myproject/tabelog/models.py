from django.db import models
from django.contrib.auth.models import AbstractUser #追加

class CustomUser(AbstractUser):
    class Meta:
        verbose_name_plural = 'CustomUser'