from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, UserManager)
from django.core.validators import MinLengthValidator
from django.db import models

from users.validators import no_bad_symbols_validator


class CustomUserManager(BaseUserManager):
    def create_superuser(
            self, email, username, first_name, last_name,
            password, **other_fields
    ):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if not other_fields.get("is_staff"):
            raise ValueError("Отказано в доступе")

        if not other_fields.get("is_superuser"):
            raise ValueError("Отказано в доступе")

        return self.create_user(
            email, username, first_name, last_name,
            password=password, **other_fields
        )

    def create_user(self, first_name, last_name,
                    email, password, **other_fields):

        if not email:
            raise ValueError("Укажите email!")

        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name,
            last_name=last_name, **other_fields
        )

        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Имя пользователя',
        max_length=settings.MAX_LENTH_NAME,
        unique=True,
        validators=[no_bad_symbols_validator],
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=settings.MAX_LENTH_EMAIL,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.MAX_LENTH_NAME,
        validators=[
            MinLengthValidator(
                settings.MIN_LENTH_NAME,
                message=(
                    f'Имя должно содержать не '
                    f'менее {settings.MIN_LENTH_NAME} символов.'
                )
            )
        ]
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.MAX_LENTH_NAME,
        validators=[
            MinLengthValidator(
                settings.MIN_LENTH_NAME,
                message=(
                    f'Фамилия должна содержать не '
                    f'менее {settings.MIN_LENTH_NAME} символов.'
                )
            )
        ]
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('email',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user_mail'),
            models.CheckConstraint(
                check=~models.Q(username__iexact='me'),
                name='username_not_me'
            )
        ]

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.email


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique follow',
            )
        ]

    def __str__(self):
        return f'{self.user} ---> {self.author}'
