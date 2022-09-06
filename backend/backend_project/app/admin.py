from django.contrib import admin

from app.models import (
    FavoriteRecipe, Ingredient,
    #IngredientUnit, MeasureUnit,
    Recipe, ShoppingCart, Subscription, Tag, User
)


class IngredientAdmin(admin.ModelAdmin):

    list_display = ['display_name', 'display_unit']
    search_fields = ['name__name']

    def display_name(self, obj):
        return obj.name.name

    def display_unit(self, obj):
        return obj.measurement_unit.name


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('in_favorites',)
    list_display = ['author', 'name', 'in_favorites']
    search_fields = ['author__username', 'name', 'tag__name']
    empty_value_display = '-пусто-'

    def in_favorites(self, obj):
        return FavoriteRecipe.objects.filter(recipe=obj).count()


admin.site.register(FavoriteRecipe)
admin.site.register(Ingredient, IngredientAdmin)
# admin.site.register(IngredientUnit)
# admin.site.register(MeasureUnit)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingCart)
admin.site.register(Subscription)
admin.site.register(Tag)
admin.site.register(User)
