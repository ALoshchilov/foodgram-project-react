import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from django.contrib.auth import get_user_model
# from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfgen import canvas
from rest_framework import mixins, status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import IngredientFilter, RecipeFilter
from .paginators import PageLimitPagination
from .permissions import Author, Follower, ReadOnly


from .serializers import (
    UserSerializer, ChangePasswordSerializer, TagSerializer,
    IngredientUnitSerializer, RecipePostSerializer,
    RecipeGetSerializer, SubscriptionGetSerializer,
    SubscriptionRecipeSerializer
)
from app.models import (
    Tag, Ingredient, Recipe, Subscription,
    FavoriteRecipe, ShoppingCart
    # RecipeCart
)

User = get_user_model()


# Вью-сеты эндпойнтов для работы с пользователями

class CustomUserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """View-set для эндпоинта users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UsersMeApiView(APIView):
    """Отдельно описываем поведение для users/me."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Получаем себя при обращении на users/me."""

        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)


class ChangePasswordView(CreateAPIView):
    """Представление для эндпоинта смены пароля пользователя."""

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not user.check_password(
                serializer.data.get("current_password")
        ):
            return Response(
                {
                    'status': 'Error',
                    'message': 'current password is wrong!',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(
            {
                'status': 'Success',
                'message': 'password updated successfully',
            },
            status=status.HTTP_204_NO_CONTENT,
        )

# Вью-сеты эндпойнтов, участвующих в создании и получении рецепта


class TagViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Представление для эндпоинта Tag."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Представление для эндпоинта Ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientUnitSerializer

    permission_classes = (AllowAny,)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для эндпоинта Рецептов."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeGetSerializer

    permission_classes = [Author | ReadOnly]

    pagination_class = PageLimitPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags', 'author',)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipePostSerializer
        return RecipeGetSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # По ТЗ - Показывать только рецепты, находящиеся в списке избранного.
        if self.request.query_params.get('is_favorited'):
            favorites = FavoriteRecipe.objects.filter(
                user=self.request.user
            ).values_list('recipe__id', flat=True)
            queryset = Recipe.objects.filter(id__in=favorites)
            return queryset

        # По ТЗ - Показывать только рецепты, находящиеся в списке покупок.
        if self.request.query_params.get('is_in_shopping_cart'):
            in_cart = ShoppingCart.objects.filter(
                user=self.request.user
            ).values_list('recipe__id', flat=True)
            queryset = Recipe.objects.filter(id__in=in_cart)
            return queryset
        return Recipe.objects.all()

# Вью-сеты для подписок


class SubscribtionPostDeleteView(APIView):

    permission_classes = [Follower | ReadOnly]

    def post(self, request, **kwargs):
        author = get_object_or_404(User, id=self.kwargs["id"])
        if author == self.request.user:
            return Response(
                {
                    'status': 'Error',
                    'message': 'you cannot follow yourself',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription, created = Subscription.objects.get_or_create(
            user=self.request.user, author=author
        )
        if not created:
            return Response(
                {
                    'status': 'Error',
                    'message': 'you have already followed the author',
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
                'status': 'Success',
                'message': 'you have unfollowed the author',
            },
            status=status.HTTP_204_NO_CONTENT
        )


class SubscribtionGetViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

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
        serializer = SubscriptionRecipeSerializer(recipe)
        favorite, created = FavoriteRecipe.objects.get_or_create(
            user=self.request.user, recipe=recipe
        )
        if not created:
            return Response(
                'The recipe is already in favorites',
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
class CartPostDestroyView(APIView):
    """Представление для добавления и удаления из корзины."""

    def post(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs["id"])
        shopping_list, created = ShoppingCart.objects.get_or_create(
            user=self.request.user, recipe=recipe
        )
        if not created:
            return Response(
                {
                    'status': 'Error',
                    'message': 'the recipe is already in your shopping list',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        shopping_list.save()
        serializer = SubscriptionRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, requets, **kwargs):
        get_object_or_404(
            ShoppingCart,
            user=self.request.user,
            recipe=get_object_or_404(Recipe, id=self.kwargs["id"])
        ).delete()
        return Response(
            {
                'status': 'Success',
                'message': 'you have removed the recipe from your shopping list',
            },
            status=status.HTTP_204_NO_CONTENT
        )


class CartDownloadView(APIView):
    """Представление для формирования и скачивания списка покупок."""

    def get(self, request, **kwargs):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)

        line = 800
        pdfmetrics.registerFont(TTFont(
            'DejaVuSerif', 'DejaVuSerif.ttf', 'UTF-8'
        ))
        p.setFont('DejaVuSerif', 20)
        p.drawString(15, line, "Список покупок.")

        recipes = ShoppingCart.objects.filter(
            user=self.request.user
        ).values_list('recipe__id', flat=True)
        recipes
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
