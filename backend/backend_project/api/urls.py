from django.urls import include, re_path, path
from rest_framework.routers import DefaultRouter

from .views import (
    CustomUserViewSet, UsersMeApiView, ChangePasswordView, TagViewSet,
    IngredientViewSet, RecipeViewSet, SubscriptionPostDeleteView,
    SubscriptionGetViewSet,
    FavoritePostDeleteView,
    ShoppingCartPostDeleteView,
    DownloadShoppingCartView
)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('users', CustomUserViewSet, 'Users')
router_v1.register('tags', TagViewSet, 'Tags')
router_v1.register('ingredients', IngredientViewSet, 'Ingredients')
router_v1.register('recipes', RecipeViewSet, 'Recipes')


urlpatterns = [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    re_path(
        r'users/(?P<id>\d+)/subscribe', SubscriptionPostDeleteView.as_view()
    ),
    path('users/set_password/', ChangePasswordView.as_view()),
    path('users/me/', UsersMeApiView.as_view()),

    re_path(
        r'recipes/(?P<id>\d+)/favorite', FavoritePostDeleteView.as_view()
    ),
    re_path(
        r'recipes/(?P<id>\d+)/shopping_cart',
        ShoppingCartPostDeleteView.as_view()
    ),

    path(
        'users/subscriptions/', SubscriptionGetViewSet.as_view({'get': 'list'})
    ),

    path(
        'recipes/download_shopping_cart/', DownloadShoppingCartView.as_view()
    ),
    path('', include(router_v1.urls)),
]
