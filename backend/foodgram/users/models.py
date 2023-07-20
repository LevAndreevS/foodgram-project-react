from django.contrib.auth.models import AbstractUser
from django.db import models
from foodgram import settings
from groceryassistant.validators import validate_forbidden_characters


class User(AbstractUser):
    """
    Модель пользователя платформы.
    Используется для аутентификации Django.
    """
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=settings.EMAIL_LENGTH,
        unique=True,
        blank=False,
    )
    username = models.CharField(
        verbose_name='Логин',
        max_length=settings.MAX_LENGTH,
        unique=True,
        blank=False,
        validators=[validate_forbidden_characters],
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.MAX_LENGTH,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.MAX_LENGTH,
        blank=False
    )
    password = models.CharField(
        max_length=settings.MAX_LENGTH,
        blank=False,
    )

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
        ordering = ('username',)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return (
            f'{self.username[:settings.NUMBER_OF_DISPLAY_DIGITS]} '
            f'{self.email}'
        )


class Follow(models.Model):
    """Подписка на пользователей."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name_plural = 'Подписки на авторов'
        verbose_name = 'Подписка на авторов'
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_follower')
        ]

    def __str__(self):
        return f'{self.user} подписался на {self.author}'
