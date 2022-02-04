from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (AbstractUser)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import ugettext_lazy as _

from user.utils import USER_TYPE, CONSUMER


class UserManager(BaseUserManager):

    def create_user(self, username, password=None):
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if password is None:
            raise TypeError('Пароль не должен быть пустым')

        username = None
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    role = models.CharField(max_length=20, default=CONSUMER, choices=USER_TYPE, verbose_name="Роль")
    full_name = models.CharField(max_length=50, blank=False, verbose_name='Фио')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return f'{self.full_name}'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def get_name(self):
        if self.full_name:
            return self.full_name
        else:
            return self.username
