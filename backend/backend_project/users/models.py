from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя"""

    email = models.EmailField(
        unique=True,
        max_length=254,
        validators=[EmailValidator],
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'password']

    @property
    def is_admin(self):
        return self.is_staff

    class Meta:
        ordering = ['email']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
