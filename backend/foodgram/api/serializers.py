from rest_framework import serializers

from recipes.models import Recipe, Tag, Ingredient
from users.models import User
import base64
from django.core.files.base import ContentFile


ROLE_CHOICES = [
    (User.USER, User.USER),
    (User.MODERATOR, User.MODERATOR),
    (User.ADMIN, User.ADMIN),
]


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    slug = serializers.RegexField('^[-a-zA-Z0-9_]+$')

    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    image = Base64ImageField(required=False, allow_null=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientSerializer(many=True)

    class Meta:
        fields = (
            'id',
            'author',
            'name',
            'image',
            'text',
            'ingredients',
            'tags',
            'cooking_time')
        model = Recipe


class RegistUserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(required=False, read_only=True)
    role = serializers.CharField(default='user')
    username = serializers.RegexField(
        "^[\\w.@+-]+", max_length=150, required=True
    )
    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'role',
            'token',
            'first_name',
            'last_name',
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать `me` как имя!'
            )
        return username


class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES, default='user')
    username = serializers.RegexField(
        '^[\\w.@+-]+', max_length=150, required=True
    )
    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'token',
            'first_name',
            'last_name',
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_username(self, username):
        if username.lower() == "me":
            raise serializers.ValidationError(
                'Нельзя использовать `me` как имя!'
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует'
            )
        return username


class UserTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
