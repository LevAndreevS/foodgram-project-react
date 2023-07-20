
from django.db import models
from foodgram import settings
from groceryassistant.validators import (validate_amount,
                                         validate_cooking_time,
                                         validate_forbidden_characters)
from users.models import User


class Tag(models.Model):
    """Модель цветовых тэгов: завтрак, обед, ужин"""
    name = models.CharField(
        verbose_name='Название тега',
        max_length=settings.NAME_LENGTH,
    )
    color = models.CharField(
        max_length=settings.COLOR_LENGTH,
        verbose_name='Цвет в HEX',
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=settings.SLUG_LENGTH,
        unique=True,
        validators=[validate_forbidden_characters]
    )

    class Meta:
        verbose_name_plural = 'Тэги'
        verbose_name = 'Тэг'

    def __str__(self):
        return f'{self.name[:settings.NUMBER_OF_DISPLAY_DIGITS]}'


class Ingredient(models.Model):
    """Класс, описывающий модель ингридиентов."""
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=settings.NAME_LENGTH,
    )
    measurement_unit = models.CharField(
        max_length=settings.NAME_LENGTH,
        verbose_name='Единицы измерения',
    )

    class Meta:
        verbose_name_plural = 'Ингридиенты'
        verbose_name = 'Ингридиент'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_name_measurement')]

    def __str__(self):
        return (
            f'{self.name[:settings.NUMBER_OF_DISPLAY_DIGITS]} '
            f'{self.measurement_unit}'
        )


class RecipeList(models.Model):
    """Класс, описывающий модель рецептов."""
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингридиенты',
        through='IngredientInRecipe',
    )
    name = models.CharField(
        max_length=settings.NAME_LENGTH,
        verbose_name='Название рецепта',
        blank=False,
    )
    image = models.ImageField(
        'Картинка',
        upload_to='groceryassistant/images/',
        blank=True,
    )
    text = models.TextField(
        verbose_name='Описание блюда',
        blank=False,
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[validate_cooking_time],
    )

    class Meta:
        verbose_name_plural = 'Рецепты'
        verbose_name = 'Рецепт'

    def __str__(self):
        return f'Автор: {self.author} рецепт: {self.name}'


class IngredientInRecipe(models.Model):
    """Кастомная модель связи ингредиентов и рецептов"""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientinrecipe',
    )
    recipe = models.ForeignKey(
        RecipeList,
        on_delete=models.CASCADE,
        related_name='ingredientinrecipe',
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        default=0,
        validators=[validate_amount]

    )

    class Meta:
        verbose_name_plural = 'Количество ингредиентов'
        verbose_name = 'Количество ингредиента'
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique ingredient')]

    def __str__(self):
        return f'{self.amount} {self.ingredient}'


class Favoritelist(models.Model):
    """Список избранного."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        RecipeList,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique favoritelist')]

    def __str__(self):
        return (
            f'Пользователь: {self.user}'
            f'избранный рецепт: {self.recipe.name}'
        )


class Shoppinglist(models.Model):
    """Список покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        RecipeList,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name_plural = 'Список покупок'
        verbose_name = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique recipe shoppinglist')]

    def __str__(self):
        return (
            f'Пользователь: {self.user} добавил'
            f'{self.recipe.name} в список покупок'
        )
