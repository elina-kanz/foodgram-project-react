from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField('Имя пользователя', max_length=150,
                                unique=True, db_index=True)
    email = models.EmailField('e-mail', unique=True)
    last_name = models.CharField('Фамилия', max_length=150, null=True)
    first_name = models.CharField('Имя', max_length=150, null=True)
    password = models.CharField('Пароль', max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return f'{self.username} {self.email}'
