import django_filters
from django_filters import rest_framework as filters

from app.models import Ingredient, Recipe


class IngredientFilter(filters.FilterSet):
    """Фильтр ингредиентов"""

    name = django_filters.CharFilter(
        field_name='name__name', lookup_expr='icontains'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    """Фильтр рецептов"""

    # ТЗ - Показывать рецепты только с указанными тегами (по slug)
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tag__slug',
        conjoined=False,
    )
    # ТЗ - Показывать рецепты только автора с указанным id.
    author = django_filters.AllValuesFilter(
        field_name='author__id'
    )

    class Meta:
        model = Recipe
        fields = ('tag',)
