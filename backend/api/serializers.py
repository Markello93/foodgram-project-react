import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from recipes.models import (Favorites, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Subscribe, User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set',
        many=True,
        read_only=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'image',
            'text', 'ingredients', 'tags',
            'cooking_time'
        )

    @staticmethod
    def recipe_create_update(validated_data, instance=None):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        if not instance:
            instance = Recipe.objects.create(**validated_data)
        else:
            instance.tags.clear()
            RecipeIngredient.objects.filter(recipe=instance).delete()
            instance.__dict__.update(validated_data)
        for ingredient_data in ingredients_data:
            ingredient = Ingredient.objects.get(id=ingredient_data['id'])
            RecipeIngredient.objects.create(recipe=instance,
                                            ingredient=ingredient,
                                            amount=ingredient_data['amount'])
        instance.tags.set(tags_data)
        instance.save()
        return instance

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        if not ingredients:
            raise serializers.ValidationError(
                'Необходим минимум один ингредиент для рецепта'
            )
        if not tags:
            raise serializers.ValidationError(
                'Необходим минимум один тег для рецепта'
            )
        ingredient_list = []
        for ingredient_item in ingredients:
            if not Ingredient.objects.filter(
                    pk=ingredient_item['id']).exists():
                raise serializers.ValidationError(
                    'Ингредиента с таким id не существует'
                )
            if int(ingredient_item['id']) in ingredient_list:
                raise serializers.ValidationError('Укажите уникальный '
                                                  'ингредиент')
            if 'amount' not in ingredient_item:
                raise serializers.ValidationError('Количество ингредиента '
                                                  'не может быть пустым')
            amount = int(ingredient_item['amount'])
            if amount <= 0 or amount > 32766:
                raise serializers.ValidationError(
                    'Укажите корректное количество ингредиента, '
                    'в диапазоне от 0,01 до 32766'
                )
            ingredient_list.append(ingredient_item['id'])
        data['ingredients'] = ingredients
        data['tags'] = tags
        return data

    def create(self, validated_data):
        return self.recipe_create_update(validated_data)

    def update(self, instance, validated_data):
        return self.recipe_create_update(validated_data, instance=instance)


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, instance):
        request = self.context.get('request')
        if not self.context.get('request').user.is_authenticated:
            return False
        return Subscribe.objects.filter(
            user=request.user, author=instance
        ).exists()

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name',
            'username', 'email', 'is_subscribed'
        )
        read_only_fields = ('email', 'username', 'first_name', 'last_name',
                            'is_subscribed')


class SubscribeSerializer(UserSerializer):
    recipes = SerializerMethodField(method_name='get_recipes')
    recipes_count = SerializerMethodField(method_name='get_recipes_count')

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')

    @staticmethod
    def get_recipes_count(instance):
        return instance.recipes.count()

    def validate(self, data):
        author_id = self.context.get(
            'request').parser_context.get('kwargs').get('id')
        author = get_object_or_404(User, id=author_id)
        user = self.context.get('request').user
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        if Subscribe.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError(
                'Нельзя подписаться на автора на которого вы уже подписаны!')
        return data

    def get_recipes(self, instance):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = instance.recipes.all()
        if limit and limit.isnumeric():
            recipes = recipes[:int(limit)]
        elif limit and not limit.isnumeric():
            raise serializers.ValidationError(
                'recipes_limit принимает только числовые значения'
            )
        return ShortRecipeSerializer(recipes, many=True).data


class RecipeViewSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    author = UserSerializer(
        read_only=True,
    )
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set',
        many=True,
        read_only=True,
    )
    image = Base64ImageField(required=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author',
                  'ingredients', 'name', 'image',
                  'text', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')

    def is_item_related(self, recipe, model):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return model.objects.filter(user=request.user, recipe=recipe).exists()

    def get_is_favorited(self, recipe):
        return self.is_item_related(recipe, Favorites)

    def get_is_in_shopping_cart(self, recipe):
        return self.is_item_related(recipe, ShoppingCart)
