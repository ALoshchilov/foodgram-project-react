from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from app.models import (
    FavoriteRecipe, Ingredient, 
    # IngredientUnit,
    Recipe, RecipeIngredient,
    RecipeTag, ShoppingCart, Subscription, Tag, User
)


WRONG_CURRENT_PASSWORD = 'Current password is wrong'
CANNOT_USER_ME_AS_USERNAME = 'You cannot use "me" as username'
NOT_UNIQUE_INGREDS = 'Ingredient {ingredient} in a recipe should be unique'
NOT_POSITIVE_COOKING_TIME = 'Cooking time should be more than 0 minutes'
NOT_POSITIVE_AMOUNT = 'Amount of {ingredient} should be more 0'


# Сериализаторы функционала, связанного с пользователями
class UserSerializer(serializers.ModelSerializer):
    """Сериализатор кастомной модели пользователя."""

    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email', 'id', 'username', 'password',
            'first_name', 'last_name', 'is_subscribed'
        )
        model = User

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'].lower(),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get('password')
        errors = dict()
        try:
            password_validation.validate_password(password=password, user=user)
        except ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        if attrs.get('username', '').lower() == 'me':
            raise serializers.ValidationError(CANNOT_USER_ME_AS_USERNAME)
        return super(UserSerializer, self).validate(attrs)

    def get_is_subscribed(self, obj):
        request = self.context.get('request', None)
        if not request:
            return False
        if isinstance(request.user, User):
            return Subscription.objects.filter(
                user=request.user, author=obj
            ).exists()
        return False


class ChangePasswordSerializer(serializers.Serializer):
    """Сериализатор для эндпоинта смены пароля пользователя."""

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        errors = dict()
        try:
            request = self.context.get('request', None)
            current_password = attrs.get('current_password')
            new_password = attrs.get('new_password')
            if not request.user.check_password(current_password):
                raise ValidationError(WRONG_CURRENT_PASSWORD)
            password_validation.validate_password(
                password=new_password, user=request.user
            )
        except ValidationError as e:
            errors['new_password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        return super(ChangePasswordSerializer, self).validate(attrs)


# Сериализаторы функционала, связанного с рецептами

class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели тегов."""

    class Meta:
        fields = '__all__'
        model = Tag


class IngredientUnitSerializer(serializers.ModelSerializer):
    """Сериализатор модели ингредиентов и единиц измерения"""

    # name = serializers.CharField(source='name.name')
    # measurement_unit = serializers.CharField(source='measurement_unit.name')

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class RecipeIngredientGetSerializer(serializers.ModelSerializer):
    """Сериализатор модели-связи для ингредиентов и рецептов"""

    id = serializers.CharField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
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
    image = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited', 'name',
            'image', 'text', 'cooking_time', 'is_in_shopping_cart'
        )
        model = Recipe

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request', None)
        if not request:
            return False
        if not isinstance(request.user, User):
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def get_is_favorited(self, obj):
        request = self.context.get('request', None)
        if not request:
            return False
        if not isinstance(request.user, User):
            return False
        return FavoriteRecipe.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def get_image(self, obj):
        return '/media/' + str(obj.image)


class RecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор для небезопасных методов модели рецептов"""

    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientPostSerializer(
        many=True, source='ingredient'
    )

    class Meta:
        fields = (
            'id', 'ingredients', 'tags', 'image', 'author', 'text',
            'cooking_time', 'name'
        )
        model = Recipe

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredient')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tag.set(tags)
        for ingredient in ingredients:
            pieces = RecipeIngredient.objects.create(
                ingredient=ingredient['id'],
                amount=ingredient['amount'])
            recipe.ingredient.add(pieces)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredient')
        tags = validated_data.pop('tags')
        super().update(instance, validated_data)
        instance.ingredient.clear()
        instance.tag.set(tags)
        for ingredient in ingredients:
            ing = RecipeIngredient.objects.create(
                ingredient=ingredient['id'],
                amount=ingredient['amount'])
            instance.ingredient.add(ing)
        return instance

    def validate(self, attrs):
        ingredients_list = []
        for ingredient_piece in attrs.get('ingredient'):
            ingredient, amount_info = list(ingredient_piece.items())
            name = ingredient[1].name
            amount = int(amount_info[1])
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    NOT_UNIQUE_INGREDS.format(ingredient=name)
                )
            ingredients_list.append(ingredient)
            if amount <= 0:
                raise serializers.ValidationError(
                    NOT_POSITIVE_AMOUNT.format(ingredient=name)
                )
        if int(attrs.get('cooking_time')) <= 0:
            raise serializers.ValidationError(NOT_POSITIVE_COOKING_TIME)
        return attrs


# Сериализаторы подписок
class RecipeNestedSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return '/media/' + str(obj.image)

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class SubscriptionGetSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source='recipes.count', read_only=True
    )
    is_subscribed = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        queryset = obj.recipes.all()[:self.context.get('recipes_limit', None)]
        serializer = RecipeNestedSerializer(queryset, many=True)
        return serializer.data

    def get_is_subscribed(self, obj):
        request = self.context.get('request', None)
        if not request:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()

    class Meta:

        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )
        model = User
