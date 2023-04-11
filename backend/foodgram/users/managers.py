from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    def create_user(
        self,
        username,
        email,
        password=None,
        role=None,
        last_name=None,
        first_name=None,
    ):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have an email address')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=role,
            last_name=last_name,
            first_name=first_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username,
        email,
        password,
        role=ADMIN,
        last_name=None,
        first_name=None,
    ):
        if password is None:
            raise TypeError('Superusers should have a password')
        user = self.create_user(
            username,
            email,
            password,
            role=role,
            last_name=last_name,
            first_name=first_name,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
