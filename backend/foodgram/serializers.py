import base64
import webcolors

from django.core.files.base import ContentFile
from rest_framework import serializers

from foodgram.models import (Ingredient, Recipe, Tag, IngredientRecipe,
                             Favorite, ShoppingCart)
from users.serializers import CustomUserSerializer


class Hex2NameColor(serializers.Field):
    """Проверка HEX-кода цвета."""
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class Base64ImageField(serializers.ImageField):
    """Декодирование картинки."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    """Ингредиенты."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = '__all__',


class TagSerializer(serializers.ModelSerializer):
    """Теги."""
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = '__all__',


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Количество ингредиентов."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class CreateIngredientSerializer(serializers.ModelSerializer):
    """Добавление ингредиентов в рецепт."""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeGetSelializer(serializers.ModelSerializer):
    """Просмотр рецептов."""
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True,
                                             source='amounts')
    tags = TagSerializer(many=True, read_only=True)
    is_favorite = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorite',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous or not request:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj).exists()

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous or not request:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()


class RecipePostSelializer(serializers.ModelSerializer):
    """Создание рецепта."""
    image = Base64ImageField(required=False, allow_null=True)
    ingredients = CreateIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name', 'text',
                  'cooking_time')

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientRecipe.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount'])

        return recipe

    def create_tags(self, tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(ingredients, recipe)
        self.create_tags(tags, recipe)
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeGetSelializer(instance, context=context).data

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientRecipe.objects.filter(recipe=instance).delete()
        self.create_ingredients(validated_data.pop('ingredients'), instance)
        self.create_tags(validated_data.pop('tags'), instance)
        return super().update(instance, validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    """Список избранного."""
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = Base64ImageField(required=False, allow_null=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Favorite
        fields = ('user', 'recipe', 'id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            raise serializers.ValidationError({
                'errors': 'Уже в избранном.'
            })
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Список покупок."""
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = Base64ImageField(required=False, allow_null=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe', 'id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if ShoppingCart.objects.filter(user=request.user,
                                       recipe=recipe).exists():
            raise serializers.ValidationError({
                'errors': 'Этот рецепт уже в корзине.'
            })
        return data
