from api.permissions import IsAdminOrAuthorOrReadOnly, IsAdminOrReadOnly
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Subcribtion, Tag)
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from users.models import User

from .filters import RecipeFilter
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RegisterUserSerializer,
                          ShoppingCartSerializer, SubscribeSerializer,
                          SubscribtionsSerializer, TagSerializer,
                          UserSerializer)


class CreateListRetrieveSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    pass


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly, )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly, )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter

    @action(detail=True, methods=('post',),
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        data = {
            'user': request.user.pk,
            'recipe': pk,
        }
        serializer = FavoriteSerializer(data=data,
                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        get_object_or_404(Favorite, user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('post',),
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk):
        data = {
            'user': request.user.pk,
            'recipe': pk,
        }
        serializer = ShoppingCartSerializer(data=data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_list = {}
        ingredients = RecipeIngredient.objects.filter(
            recipe__in_shopping_cart__user=request.user).order_by(
            'ingredient__name').values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        shopping_list = 'Список покупок: '
        for ingredient in ingredients:
            shopping_list += (
                f'\n {ingredient["ingredient__name"]} '
                f'({ingredient["ingredient__measurement_unit"]}) — '
                f'{ingredient["amount"]}')
        file = 'shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file}.txt"'
        return response

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        get_object_or_404(
            ShoppingCart, user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(CreateListRetrieveSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterUserSerializer
        return UserSerializer

    @action(detail=False,
            permission_classes=[permissions.IsAuthenticated],
            methods=['post'])
    def subscribe(self, request, pk):
        user = request.user
        data = {
            'user': user.pk,
            'author': pk,
        }
        serializer = SubscribeSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        author = get_object_or_404(User, pk=pk)
        Subcribtion.objects.create(user=user, author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        get_object_or_404(Subcribtion, user=request.user,
                          author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribtionsSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
