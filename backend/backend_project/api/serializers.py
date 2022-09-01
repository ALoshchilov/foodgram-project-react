from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField

from app.models import (
    Tag, Ingredient, IngredientUnit, RecipeIngredient,
    Recipe, RecipeTag, ShoppingCart, Subscription, FavoriteRecipe,
    # RecipeCart
)

User = get_user_model()

# Сериализаторы функционала, связанного с пользователями


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для кастомной модели пользователя."""

    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField('check_subscription')

    class Meta:
        fields = (
            'email', 'id', 'username', 'password',
            'first_name', 'last_name', 'is_subscribed'
        )
        model = User

    def check_subscription(self, obj):
        request = self.context.get('request', None)
        if not request:
            return False
        if isinstance(request.user, User):
            return Subscription.objects.filter(
                user=request.user, author=obj
            ).exists()
        return False

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'].lower(),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Сериализатор для эндпоинта смены пароля пользователя."""

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User


# Сериализаторы функционала, связанного с рецептами

class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели тегов."""

    class Meta:
        fields = ('__all__')
        model = Tag


class IngredientUnitSerializer(serializers.ModelSerializer):
    """Сериализатор модели ингредиентов и единиц измерения"""

    name = serializers.CharField(source='name.name')
    measurement_unit = serializers.CharField(source='measurement_unit.name')

    class Meta:
        fields = ('__all__')
        model = IngredientUnit


class RecipeIngredientGetSerializer(serializers.ModelSerializer):
    """Сериализатор модели-связи для ингредиентов и рецептов"""

    id = serializers.CharField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit.name'
    )

    class Meta:
        fields = ('id', 'amount', 'name', 'measurement_unit')
        model = RecipeIngredient


class RecipeIngredientPostSerializer(serializers.ModelSerializer):
    """Сериализатор модели-связи для создания записей ингредиент-рецепт"""

    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        fields = ('id', 'amount')
        model = RecipeIngredient


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор для безопасных методов модели рецептов"""

    tags = TagSerializer(many=True, read_only=True, source='tag')
    author = UserSerializer()
    ingredients = RecipeIngredientGetSerializer(
        many=True, read_only=True, source='ingredient'
    )
    image = serializers.SerializerMethodField('get_image_url')
    is_favorited = serializers.SerializerMethodField('check_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(
        'check_is_in_shopping_cart'
    )

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited', 'name',
            'image', 'text', 'cooking_time', 'is_in_shopping_cart'
        )
        model = Recipe

    def check_is_in_shopping_cart(self, obj):
        request = self.context.get('request', None)
        if not request:
            return False
        if not isinstance(request.user, User):
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def check_is_favorited(self, obj):
        request = self.context.get('request', None)
        if not request:
            return False
        if not isinstance(request.user, User):
            return False
        return FavoriteRecipe.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def get_image_url(self, obj):
        return '/media/' + str(obj.image)


class RecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор для небезопасных методов модели рецептов"""

    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    image = Base64ImageField()
    author = SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    ingredients = RecipeIngredientPostSerializer(
        many=True,
        source='ingredient'
    )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredient')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            pieces = RecipeIngredient.objects.create(
                ingredient=ingredient['id'],
                amount=ingredient['amount'])
            recipe.ingredient.add(pieces)
        for tag in tags:
            RecipeTag.objects.create(recipe=recipe, tag=tag)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredient')
        tags = validated_data.pop('tags')
        super().update(instance, validated_data)
        instance.ingredient.select_related().all().delete()
        RecipeTag.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            ing = RecipeIngredient.objects.create(
                ingredient=ingredient['id'],
                amount=ingredient['amount'])
            instance.ingredient.add(ing)
        for tag in tags:
            RecipeTag.objects.create(recipe=instance, tag=tag)
        return instance

    class Meta:
        fields = (
            'ingredients', 'tags', 'image', 'author', 'text',
            'cooking_time', 'name'
        )
        model = Recipe


# Сериализаторы подписок
# Переименовать, хреновый нейминг вышел
class SubscriptionRecipeSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для рецептов в подписках."""

    image = serializers.SerializerMethodField('get_image_url')

    def get_image_url(self, obj):
        return '/media/' + str(obj.image)

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class SubscriptionGetSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""

    recipes = serializers.SerializerMethodField('get_recipes')
    recipes_count = serializers.IntegerField(
        source='recipes.count', read_only=True
    )

    def get_recipes(self, obj):
        queryset = obj.recipes.all()[:self.context.get('recipes_limit', None)]
        serializer = SubscriptionRecipeSerializer(queryset, many=True)
        return serializer.data

    class Meta:

        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'recipes',
            'recipes_count'
        )
        model = User


# Пока скопирую в чердак, вдруг пригодится

# class RecipeTagSerializer(serializers.ModelSerializer):
#     """Сериализатор модели-связи для тегов и рецептов"""

#     class Meta:
#         fields = ('__all__')
#         model = RecipeTag


# class MeasurementUnitSerializer(serializers.ModelSerializer):
#     """Сериализатор модели единиц измерения"""

#     class Meta:
#         fields = ('name',)
#         model = MeasureUnit


# class IngredientSerializer(serializers.ModelSerializer):
#     """Сериализатор модели ингредиентов"""

#     name = serializers.CharField()

#     class Meta:
#         fields = ('name',)
#         model = Ingredient
