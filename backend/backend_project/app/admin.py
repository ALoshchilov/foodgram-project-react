from django.contrib import admin

from .models import (
    Tag, Recipe, MeasureUnit, IngredientUnit, Ingredient, Subscription,
    RecipeIngredient, RecipeTag, FavoriteRecipe
    # RecipeCart, 
)

admin.site.register(Tag)
# admin.site.register(Recipe, RecipeAdmin)
admin.site.register(MeasureUnit)
# admin.site.register(IngredientUnit, IngredientAdmin)
admin.site.register(IngredientUnit)
admin.site.register(Subscription)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeTag)
# admin.site.register(RecipeCart)
# admin.site.register(RecipeFavorite)
