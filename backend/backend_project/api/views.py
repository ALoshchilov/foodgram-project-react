import io

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import mixins, status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import RecipeFilter
from .paginators import PageLimitPagination
from .permissions import Author, Follower, ReadOnly
from .serializers import (
    ChangePasswordSerializer, IngredientUnitSerializer, RecipeGetSerializer,
    RecipeNestedSerializer, RecipePostSerializer, SubscriptionGetSerializer,
    TagSerializer, UserSerializer
)
from app.models import (
    FavoriteRecipe, Ingredient, Recipe,  ShoppingCart, Subscription, Tag, User
)


ERROR_STATUS = 'Error'
SUCCESS_STATUS = 'Success'
PASSWORD_CHANGED = ' password updated successfully'
CAN_NOT_FOLLOW_YOURSELF = ' you cannot follow yourself'
ALREADY_FOLLOW = ' you have already followed the author'
UNFOLLOW_AUTHOR = ' you have unfollowed the author'
ALREADY_IN_FAVORITES = ' the recipe is already in favorite'
ALREADY_IN_SHOPPING_LIST = 'the recipe is already in your shopping list'
REMOVED_FROM_SHOPPING_LIST = (
    'you have removed the recipe from your shopping list'
)


# Вью-сеты эндпойнтов для работы с пользователями

class CustomUserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UsersMeApiView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):

        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)


class ChangePasswordView(CreateAPIView):

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(
            {
                'status': SUCCESS_STATUS,
                'message': PASSWORD_CHANGED,
            },
            status=status.HTTP_204_NO_CONTENT,
        )


# Вью-сеты эндпойнтов, участвующих в создании и получении рецепта

class TagViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):

    serializer_class = IngredientUnitSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        name_param = self.request.query_params.get('name', None)
        if name_param:
            return Ingredient.objects.filter(name__name__icontains=name_param)
        return Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    serializer_class = RecipeGetSerializer
    permission_classes = [Author | ReadOnly]
    pagination_class = PageLimitPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipePostSerializer
        return RecipeGetSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SubscriptionPostDeleteView(APIView):

    permission_classes = [Follower | ReadOnly]

    def post(self, request, **kwargs):
        author = get_object_or_404(User, id=self.kwargs["id"])
        if author == self.request.user:
            return Response(
                {
                    'status': ERROR_STATUS,
                    'message': CAN_NOT_FOLLOW_YOURSELF,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription, created = Subscription.objects.get_or_create(
            user=self.request.user, author=author
        )
        if not created:
            return Response(
                {
                    'status': ERROR_STATUS,
                    'message': ALREADY_FOLLOW,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription.save()
        serializer = SubscriptionGetSerializer(author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, requets, **kwargs):
        get_object_or_404(
            Subscription,
            user=self.request.user,
            author=get_object_or_404(User, id=self.kwargs["id"])
        ).delete()
        return Response(
            {
                'status': SUCCESS_STATUS,
                'message': UNFOLLOW_AUTHOR,
            },
            status=status.HTTP_204_NO_CONTENT
        )


class SubscriptionGetViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = SubscriptionGetSerializer
    pagination_class = PageLimitPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.filter(
            id__in=self.request.user.follower.all().values_list(
                'author__id', flat=True
            )
        )
        return queryset

    # По ТЗ  - Количество объектов внутри поля recipes.
    # Передача в сериалайзер нормализованного значения через доп. контекст.
    def get_serializer_context(self):
        context = super().get_serializer_context()
        recipes_limit = self.request.query_params.get('recipes_limit')
        if (
            recipes_limit and recipes_limit.isnumeric()
            and int(recipes_limit) >= 0
        ):
            context['recipes_limit'] = int(recipes_limit)
        return context


# Вью-сет добавления и удаления из избранного
class FavoritePostDeleteView(APIView):

    def post(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs["id"])
        serializer = RecipeNestedSerializer(recipe)
        favorite, created = FavoriteRecipe.objects.get_or_create(
            user=self.request.user, recipe=recipe
        )
        if not created:
            return Response(
                {
                    'status': ERROR_STATUS,
                    'message': ALREADY_IN_FAVORITES,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        favorite.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, requets, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs["id"])
        favorite = get_object_or_404(
            FavoriteRecipe, user=self.request.user, recipe=recipe
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Вью - сеты функционла корзины
class ShoppingCartPostDeleteView(APIView):

    def post(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs["id"])
        shopping_list, created = ShoppingCart.objects.get_or_create(
            user=self.request.user, recipe=recipe
        )
        if not created:
            return Response(
                {
                    'status': ERROR_STATUS,
                    'message': ALREADY_IN_SHOPPING_LIST,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        shopping_list.save()
        serializer = RecipeNestedSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, requets, **kwargs):
        get_object_or_404(
            ShoppingCart,
            user=self.request.user,
            recipe=get_object_or_404(Recipe, id=self.kwargs["id"])
        ).delete()
        return Response(
            {
                'status': SUCCESS_STATUS,
                'message': REMOVED_FROM_SHOPPING_LIST,
            },
            status=status.HTTP_204_NO_CONTENT
        )


class DownloadShoppingCartView(APIView):

    def get(self, request, **kwargs):
        line = 800

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        pdfmetrics.registerFont(TTFont(
            'DejaVuSerif', 'DejaVuSerif.ttf', 'UTF-8'
        ))
        p.setFont('DejaVuSerif', 20)
        p.drawString(15, line, "Список покупок.")
        line -= 40
        p.setFont('DejaVuSerif', 12)

        recipes = Recipe.objects.filter(
            id__in=ShoppingCart.objects.filter(
                user=self.request.user
            ).values_list('recipe__id', flat=True)
        )
        shopping_list = {}
        for recipe in recipes:
            for ingredient in recipe.ingredient.all():
                key = (
                    f'{str(ingredient.ingredient.name)}'
                    f', {str(ingredient.ingredient.measurement_unit.name)}'
                )
                if shopping_list.get(key):
                    shopping_list[key] += ingredient.amount
                else:
                    shopping_list[key] = ingredient.amount
        for ingredient, amount in sorted(shopping_list.items()):
            line -= 20
            p.drawString(
                10, line, f'{ingredient}........{amount}'.capitalize()
            )
        p.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True, filename='shopping-list.pdf'
        )
