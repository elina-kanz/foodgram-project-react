from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Ингредиент', max_length=200)
    measurement_unit = models.CharField(verbose_name='Единицы измерения',
                                        max_length=200)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(verbose_name='Тег', max_length=200, unique=True)
    color = models.CharField(verbose_name='Цвет выделения тега', max_length=7,
                             unique=True)
    slug = models.SlugField(verbose_name='Слаг тега', max_length=200,
                            unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Автор рецепта',
        on_delete=models.CASCADE, related_name='recipes'
    )
    name = models.CharField(verbose_name='Название блюда', max_length=200)
    image = models.ImageField(
        verbose_name='Картинка к рецепту',
        upload_to='recipes/', null=True, blank=True
    )
    text = models.TextField(verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='Ингредиенты',
                                         related_name='recipes',
                                         through='RecipeIngredient')
    tags = models.ManyToManyField(Tag, verbose_name='Теги',
                                  related_name='recipes',
                                  through='RecipeTag')
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)],
                                       verbose_name='Время готовки')

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name='Для каких рецептов',
                               related_name='ingredient',
                               on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredient,
                                    verbose_name='Ингредиенты в рецепте',
                                    related_name='recipe',
                                    on_delete=models.CASCADE)

    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество'
    )

    def __str__(self):
        return f'{self.recipe} {self.ingredients}'

    class Meta:
        unique_together = ('recipe', 'ingredients')


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name='Для каких рецептов',
                               on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, verbose_name='Теги', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe} {self.tag}'

    class Meta:
        unique_together = ('recipe', 'tag')
