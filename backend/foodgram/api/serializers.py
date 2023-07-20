
from api.utils import Base64ImageField
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from djoser.serializers import (PasswordSerializer, UserCreateSerializer,
                                UserSerializer)
from groceryassistant.models import (Favoritelist, Ingredient,
                                     IngredientInRecipe, RecipeList,
                                     Shoppinglist, Tag)
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator
from users.models import User


class MyUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password')


class UserPasswordSerializer(PasswordSerializer):
    """Сериализатор для проверки пароля на совпадение и неверного ввода."""
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context.get('request').user
        if data['new_password'] == data['current_password']:
            raise serializers.ValidationError(
                {"new_password": "Пароли не должны совпадать"}
            )
        check_current = check_password(
            data['current_password'],
            user.password
        )
        if check_current is False:
            raise serializers.ValidationError(
                {"current_password": "Введен неверный пароль"}
            )
        return data


class MyUserListSerializer(UserSerializer):
    """Сериализатор для работы с информацией о пользователях."""
    is_subscribed = SerializerMethodField(method_name='get_is_subscribed')

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated and obj.following.filter(
            user=request.user).exists())


class FollowsListSerializer(MyUserListSerializer):
    """Сериализатор для предоставления информации о подписках пользователя."""
    recipes_count = SerializerMethodField(method_name='get_recipes_count')
    recipes = SerializerMethodField(method_name='get_recipes')

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'recipes', 'recipes_count')
        read_only_fields = ('email', 'username',
                            'first_name', 'last_name')

    def validate(self, data):
        author_id = self.context.get(
            'request').parser_context.get('kwargs').get('id')
        author = get_object_or_404(User, id=author_id)
        user = self.context.get('request').user
        if user.follower.filter(author=author_id).exists():
            raise ValidationError(
                detail='Вы уже подписаны на этого пользователя',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if user == author:
            raise ValidationError(
                detail='Нельзя подписываться на себя!',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data

    def get_recipes(self, obj):
        request = self.context.get('request')
        try:
            limit = request.GET.get('recipes_limit')
        except AttributeError:
            limit = False
        author = get_object_or_404(User, username=obj.username)
        recipes = RecipeList.objects.filter(author=author)
        if limit:
            recipes = recipes.all()[:int(limit)]
        return RecipeShortSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        """Функция подсчета числа рецептов автора"""
        author = get_object_or_404(User, username=obj.username)
        return RecipeList.objects.filter(author=author).count()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с тегами."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')

    def validate(self, data):
        for key, value in data.items():
            data[key] = value.sttrip('#').lower()
        return data


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с ингредиентами."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientReadSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации об ингредиентах.
    Используется при работе с рецептами.
    """
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class AddIngredientForRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиентов.
    Используется при работе с рецептами.
    """
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount',)


class GetRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о рецепте."""
    author = MyUserListSerializer(read_only=True)
    tags = TagSerializer(read_only=False, many=True)
    ingredients = IngredientReadSerializer(
        many=True, read_only=True, source='ingredientinrecipe'
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )
    image = Base64ImageField(max_length=None)

    class Meta:
        model = RecipeList
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time'
                  )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and obj.favorites.filter(user=request.user).exists())

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and obj.shopping_list.filter(user=request.user).exists())


class CreateUpdateRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для добаления/обновления рецепта."""
    image = Base64ImageField(max_length=None)
    author = MyUserListSerializer(read_only=True)
    ingredients = AddIngredientForRecipeSerializer(
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        error_messages={'does_not_exist': 'Такого тега не существует'}
    )
    cooking_time = serializers.IntegerField()

    class Meta:
        model = RecipeList
        fields = (
            'id', 'author', 'tags', 'ingredients',
            'name', 'image', 'text', 'cooking_time')

    def validate_tags(self, tags):
        tags_list = []
        for tag in tags:
            if not Tag.objects.filter(id=tag.id).exists():
                raise serializers.ValidationError(
                    'Такого тега не существует')
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError(
                    'Теги должны быть уникальными')
            tags_list.append(tag)
            if len(tags_list) < settings.MIN_AMOUNT_TAG:
                raise serializers.ValidationError(
                    'Выберите хотя бы один тэг')
        return tags

    def validate_cooking_time(self, cooking_time):
        if cooking_time < settings.TIME_MIN_COOKING:
            raise serializers.ValidationError(
                'Время готовки должно быть не менее одной минуты')
        if cooking_time > settings.TIME_MAX_COOKING:
            raise serializers.ValidationError(
                'Время приготовления должно быть не более 10-ти часов')
        return cooking_time

    def validate_ingredients(self, data):
        if not data:
            raise serializers.ValidationError(
                'Добавьте ингредиенты!'
            )
        ingredients = self.data.get('ingredients')
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError(
                    'Одинаковых ингредиентов не должно быть!'
                )
            ingredients_list.append(ingredient_id)
            if int(ingredient.get('amount')) < 1:
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть больше 0')
        return data

    @classmethod
    def create_ingredients(cls, recipe, ingredients):
        for ingredient_data in ingredients:
            ingredient_list = [IngredientInRecipe(
                ingredient=ingredient_data['id'],
                amount=ingredient_data['amount'],
                recipe=recipe,
            )]
        return IngredientInRecipe.objects.bulk_create(ingredient_list)

    def create(self, validated_data):
        request = self.context.get('request', None)
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = RecipeList.objects.create(
            author=request.user, **validated_data
        )
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, recipe, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        IngredientInRecipe.objects.filter(recipe=recipe).delete()
        self.create_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)

    def to_representation(self, instance):
        return GetRecipeSerializer(
            instance, context={
                'request': self.context.get('request')
            }).data


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с краткой информацией о рецепте."""
    class Meta:
        model = RecipeList
        fields = (
            'name', 'text',
            'cooking_time', 'image',
        )


class FavoriteListSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с избранными рецептами."""
    class Meta:
        model = Favoritelist
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']
        if user.favorites.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError(
                'Этот рецепт уже в избранном!'
            )
        return data

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class ShoppingListSerializer(serializers.ModelSerializer):
    """Сериализатор для работы со списком покупок."""
    class Meta:
        model = Shoppinglist
        fields = ('recipe', 'user')

        def validate(self, data):
            user = data['user']
            if user.shopping_list.filter(recipe=data['recipe']).exists():
                raise serializers.ValidationError(
                    'Такой рецепт уже есть в корзине!'
                )

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
