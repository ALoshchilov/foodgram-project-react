from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import UniqueConstraint
from django.utils.text import slugify
from time import strftime
from transliterate import translit

User = get_user_model()


class Ingredient(models.Model):
    """Модель связи ингредиентов и единиц измерения"""

    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


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
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def save(self, *args, **kwargs):
        self.slug = slugify(
            f'{translit(self.name, "ru", reversed=True)[:136]}'
            f'{strftime("%Y%m%d%H%M%S")}'
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель связи рецептов и ингредиентов."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='pieces',
        verbose_name='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='pieces',
        verbose_name='Рецепт',
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
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'], name='unique_piece'
            ),
        ]

    def __str__(self):
        return (
            f'Ингредиент "{self.ingredient.name}" в количестве "{self.amount}'
            f' ({self.ingredient.measurement_unit})" входит в'
            f' рецепт "{self.recipe}"'
        )


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

    def __str__(self):
        return (
            f'Рецепт "{self.recipe.name}" связан с тэгом "{self.tag.name}"'
        )


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
        ordering = ['author_id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return (
            f'"{self.user.username}" подписан на "{self.author.username}"'
        )


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

    def __str__(self):
        return (
            f'Рецепт "{self.recipe.name}" в избранных у пользователя'
            f'"{self.user.username}"'
        )


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

    def __str__(self):
        return (
            f'Рецепт "{self.recipe.name}" в корзине у пользователя'
            f'"{self.user.username}"'
        )
