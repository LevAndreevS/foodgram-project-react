
from api.filtres import IngredientFilter, RecipeFilter
from api.permissions import AuthorAdminPermission
from api.serializers import (CreateUpdateRecipeSerializer,
                             FavoriteListSerializer, FollowsListSerializer,
                             GetRecipeSerializer, IngredientSerializer,
                             MyUserCreateSerializer, MyUserListSerializer,
                             ShoppingListSerializer, TagSerializer,
                             UserPasswordSerializer)
from api.utils import create_model, delete_model
from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from groceryassistant.models import (Favoritelist, Ingredient,
                                     IngredientInRecipe, RecipeList,
                                     Shoppinglist, Tag)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.models import Follow, User


class MyUserViewSet(UserViewSet):
    """Управление созданием пользователя,
    cоздание/удаление подписки на пользователя.
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_or_create_serializer_class(self):
        if self.action == 'set_password':
            return UserPasswordSerializer
        elif self.action == 'create':
            return MyUserCreateSerializer
        return MyUserListSerializer

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def get_self_page(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)

        if request.method == 'POST':
            serializer = FollowsListSerializer(
                author, data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        get_object_or_404(
            Follow, user=user, author=author
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowsListSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(ModelViewSet):
    """Получение информации о тегах."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    """Представления ингридиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    """Работа с рецептами. Создание/изменение/удаление рецепта.
    Получение информации о рецептах.
    Добавление рецептов в избранное и список покупок.
    Отправка файла со списком рецептов.
    """
    queryset = RecipeList.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = [AuthorAdminPermission]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return GetRecipeSerializer
        return CreateUpdateRecipeSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        """Работа с избранными рецептами.
        Удаление/добавление в избранное.
        """
        recipe = get_object_or_404(RecipeList, id=pk)
        error_message = 'В избранном нет этого рецепта'
        if request.method == 'POST':
            return create_model(request, recipe, FavoriteListSerializer)
        return delete_model(request, Favoritelist, recipe, error_message)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        """Работа со списком покупок.
        Удаление/добавление в список покупок.
        """
        recipe = get_object_or_404(RecipeList, id=pk)
        error_message = 'Нет такого рецепта в списке покупок'
        if request.method == 'POST':
            return create_model(request, recipe, ShoppingListSerializer)
        return delete_model(request, Shoppinglist, recipe, error_message)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        """Отправка файла со списком покупок."""
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_list__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_amount=Sum('amount'))
        shopping_list = ['Список покупок:\n']
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['ingredient_amount']
            shopping_list.append(f'\n{name} - {amount}, {unit}')
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = ('attachment;'
                                           'filename="shopping_cart.txt"')
        return response
