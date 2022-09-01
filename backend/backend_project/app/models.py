from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import UniqueConstraint

from users.models import CustomUser


class MeasureUnit(models.Model):
    """Модель единиц измерения ингредиентов"""

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения'
    )

    def __str__(self):
        return self.name


class IngredientUnit(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название ингредиента',
        help_text='Введите название'
    )
    measurement_unit = models.ManyToManyField(
        MeasureUnit,
        through='Ingredient',
        related_name='ingredients',
        verbose_name='Единицы измерения'
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель связи ингредиентов и единиц измерения"""

    name = models.ForeignKey(
        IngredientUnit,
        on_delete=models.CASCADE
    )
    measurement_unit = models.ForeignKey(
        MeasureUnit,
        on_delete=models.CASCADE
    )


class Tag(models.Model):
    """Модель тэгов"""

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Имя тега',
        help_text='Введите имя тега'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='slug'
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет тэга в HEX',
        help_text='Введите цвет тэга в HEX')

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель связи рецептов и ингредиентов."""

    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )


class Recipe(models.Model):
    """Описание модели для рецептов."""

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта'
    )
    text = models.TextField(verbose_name='Описание рецепта')
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Изображение'
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='recipes',
        through='RecipeTag',
        verbose_name='Теги'
    )
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)])
    ingredient = models.ManyToManyField(
        RecipeIngredient,
        related_name='recipes',
        verbose_name='Ингредиенты'
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    """Модель связи рецептов с тегами."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='tags'
    )
    tag = models.ForeignKey(
        Tag,
        verbose_name='Тег',
        on_delete=models.CASCADE
    )


class FavoriteRecipe(models.Model):
    """Таблица для любимых рецептов."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        constraints = [UniqueConstraint(
            fields=['recipe', 'user'],
            name='unique_recipe_favorite'
        )]


class Subscription(models.Model):
    """Модель подписок"""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор'
    )

    class Meta:
        constraints = [UniqueConstraint(
            name='unique_subscription',
            fields=['user', 'author']
        )]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class ShoppingCart(models.Model):
    """Таблица для корзины покупок."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        constraints = [UniqueConstraint(
            fields=['recipe', 'user'],
            name='unique_recipe_cart'
        )]
