from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиентов"""
    name = models.CharField(verbose_name='Ингредиент', max_length=200)
    measurement_unit = models.CharField(verbose_name='Единицы измерения',
                                        max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name', )

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(verbose_name='Название тега',
                            max_length=200, unique=True)
    color = models.CharField(verbose_name='Цвет выделения тега', max_length=7,
                             unique=True)
    slug = models.SlugField(verbose_name='Слаг тега', max_length=200,
                            unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта"""
    author = models.ForeignKey(User, verbose_name='Автор рецепта',
                               on_delete=models.CASCADE,
                               related_name='recipes', null=True)
    name = models.CharField(verbose_name='Название блюда', max_length=200)
    image = models.ImageField(verbose_name='Картинка к рецепту',
                              upload_to='recipes/', null=True, blank=True)
    text = models.TextField(verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='Ингредиенты',
                                         through='recipes.RecipeIngredient')
    tags = models.ManyToManyField(Tag, verbose_name='Теги',
                                  through='recipes.RecipeTag')
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)],
                                       verbose_name='Время готовки')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True,)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """
    Модель, связывающая рецепт и ингредиенты, через которую можно указать
    количество ингредиентов в рецепте
    """
    recipe = models.ForeignKey(Recipe, verbose_name='Для каких рецептов',
                               related_name='ingredientinrecipe',
                               on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient,
                                   verbose_name='Ингредиент в рецепте',
                                   on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'],
                                    name='unique_recipeingredientrel')]


class RecipeTag(models.Model):
    """Модель, связывающая рецепт и теги"""
    recipe = models.ForeignKey(Recipe, verbose_name='Для каких рецептов',
                               on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, verbose_name='Теги', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe} {self.tag}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique_recipetagrel')]


class Subcribtion(models.Model):
    """Модель подписок"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription')]

    def __str__(self):
        return f'{self.following} {self.follower}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorites')

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite_recipes')
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='shopping_cart')
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепты в корзине',
                               on_delete=models.CASCADE,
                               related_name='in_shopping_cart')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe_in_user_cart'
            ),
        )
