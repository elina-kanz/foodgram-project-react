from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    USER_ROLES = [
        (USER, "user"),
        (MODERATOR, "moderator"),
        (ADMIN, "admin"),
    ]
    username = models.CharField(max_length=150, unique=True, db_index=True)
    email = models.EmailField(unique=True)
    last_name = models.CharField(max_length=150, null=True)
    first_name = models.CharField(max_length=150, null=True)
    role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        default=USER,
    )
    confirmation_code = models.CharField(max_length=100, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = UserManager()

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        epoch = datetime(1970, 1, 1)
        exp_time = datetime.now() + timedelta(days=1) - epoch
        token = jwt.encode(
            {"id": self.pk, "exp": int(exp_time.total_seconds())},
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        return token.decode("utf-8")

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
