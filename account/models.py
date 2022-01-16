from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """Customized User to login with email and password
    """
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
