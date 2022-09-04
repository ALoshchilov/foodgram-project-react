from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import UniqueConstraint

User = get_user_model()


class MeasureUnit(models.Model):
    """Модель единиц измерения ингредиентов"""

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения'
    )

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

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

    class Meta:
        verbose_name = 'Наименование ингредиента'
        verbose_name_plural = 'Наименования ингредиентов'

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

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


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

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

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
        validators=[
            MinValueValidator(1)
        ],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Связь рецепта с ингредиентами'
        verbose_name_plural = 'Связи рецепта с ингредиентами'


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        User,
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
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время готовки'
    )
    ingredient = models.ManyToManyField(
        RecipeIngredient,
        related_name='recipes',
        verbose_name='Ингредиенты'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

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

    class Meta:
        verbose_name = 'Связь рецепта с тегами'
        verbose_name_plural = 'Связи рецепта с тегами'


class Subscription(models.Model):
    """Модель подписок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
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


class FavoriteRecipe(models.Model):
    """Модель любимых рецептов"""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='favorite_recipe',
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='favorite_user',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'
        constraints = [UniqueConstraint(
            fields=['recipe', 'user'],
            name='unique_user_favorite_recipe_pair'
        )]


class ShoppingCart(models.Model):
    """Модель рецептов в корзине покупок."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='shopping_recipe',
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='shopping_user',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Рецепт в корзине покупок'
        verbose_name_plural = 'Рецепты в корзине покупок'
        constraints = [UniqueConstraint(
            fields=['recipe', 'user'],
            name='unique_user_shopping_recipe_pair'
        )]
