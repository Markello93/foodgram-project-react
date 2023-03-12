from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

from users.models import User


class Tag(models.Model):
    """Модель тегов для рецептов пользователей."""
    name = models.CharField('Название тега', max_length=20, unique=True)
    color = models.CharField('Цвет тега', max_length=7, validators=[
        RegexValidator(
            regex="^#(?:[0-9a-fA-F]{3}){1,2}$",
            message='Введите цвет в формате HEX',
        )
    ], unique=True)
    slug = models.SlugField('Ссылка на тег', unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов для рецептов пользователей."""
    name = models.CharField('Название ингридиента', max_length=100)
    measurement_unit = models.CharField('Единица измерения', max_length=10)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель создания рецептов пользователями."""
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        null=True,
        related_name='recipes'
    )
    name = models.CharField('Название блюда', max_length=200)
    image = models.ImageField('Фотография блюда', upload_to='')
    text = models.CharField('Описание рецепта', max_length=2000)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(Tag)
    pub_date = models.DateTimeField(
        'Дата создания рецепта',
        auto_now_add=True,
        db_index=True,
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(
            1,
            'Время приготовления не менее 1 минуты'
        )
        ]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.name}. Автор: {self.author.username}'


class RecipeIngredient(models.Model):
    """Связанная модель для добавления ингредиентов в рецепты."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(default=1, validators=[
        MinValueValidator(0.01, 'Количество должно быть больше 0.01'),
        MaxValueValidator(32766, 'Количество должно быть меньше 32766')
    ])

    class Meta:
        verbose_name = 'Рецепт-ингредиент'
        verbose_name_plural = 'Рецепты-ингредиенты'

    def __str__(self):
        return f'{self.amount} {self.ingredient}'


class Favorites(models.Model):
    """Модель для добавления рецептов в избранное."""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты в избранном',
        related_name='fav_recipe',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='fav_user',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user', ),
                name='recipe_user_unique',
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} -> {self.recipe}'


class ShoppingCart(models.Model):
    """Модель для добавления рецептов в в корзину."""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='cart_user',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты в списке покупок',
        related_name='cart_recipes',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user', ),
                name='recipe_user_cart_unique',
            ),
        )
