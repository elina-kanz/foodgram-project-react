from django.shortcuts import get_object_or_404
from .serializers import (RecipeSerializer, TagSerializer,
                          IngredientSerializer, RegistUserSerializer,
                          UserSerializer, UserTokenSerializer)
from recipes.models import Recipe, Tag, Ingredient
from users.models import User
from django.core.mail import send_mail
from api.permissions import (IsAdmin, IsAdminOrReadOnly, IsOwnerOrReadOnly,
                             IsSelf)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.conf import settings
from rest_framework import exceptions, filters, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        response_data = {
            'username': request.data.get('username'),
            'email': request.data.get('email'),
        }
        if User.objects.filter(username=request.data.get('username')).exists():
            user_obj = User.objects.get(username=request.data.get('username'))
            if user_obj.email != request.data.get('email'):
                raise exceptions.ParseError
            send_mail(
                'confirmation code',
                user_obj.confirmation_code,
                settings.DEFAULT_MAIL,
                [user_obj.email],
            )
            return Response(response_data, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.save()
        send_mail(
            'confirmation_code',
            user_obj.confirmation_code,
            settings.DEFAULT_MAIL,
            [request.data.get('email')],
        )
        return Response(response_data, status=status.HTTP_200_OK)


class UserModelViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    def get_queryset(self):
        user_obj = self.kwargs.get('username')
        if user_obj:
            return User.objects.filter(username=user_obj)
        return User.objects.all()

    def retrieve(self, request, username=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def partial_update(self, request, username=None):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=["get", "patch"], permission_classes=[IsSelf]
    )
    def me(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)


class UserTokenView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            confirmation_code = serializer.validated_data.get(
                'confirmation_code'
            )
            user = get_object_or_404(User, username=username)
            if default_token_generator.check_token(user, confirmation_code):
                token = AccessToken.for_user(user)
                return Response(
                    {'token': f'{token}'}, status=status.HTTP_200_OK
                )
            return Response(
                {'confirmation_code': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
