from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    first_name = models.CharField('first name', max_length=150, blank=False)
    last_name = models.CharField('last name', max_length=150, blank=False)
    email = models.EmailField('email address', blank=False, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'), name='username_email_unique'
            )
        ]
        ordering = ('id',)

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """Класс Subscribe определеяет ключевые
    параметры системы подписки на авторов рецептов.
    """

    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='followed',
    )

    class Meta:
        UniqueConstraint(name='unique_subscribing', fields=['user', 'author'])
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
