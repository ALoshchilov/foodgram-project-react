import django_filters
from django_filters import rest_framework as filters

from app.models import Recipe


class RecipeFilter(filters.FilterSet):
    """Фильтр рецептов"""

    tags = django_filters.AllValuesMultipleFilter(
        field_name='tag__slug',
        conjoined=False
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    author = django_filters.AllValuesFilter(
        field_name='author__id'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorite_recipe__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_recipe__user=self.request.user)
        return queryset
