from django_filters import rest_framework as filter
from django_filters.rest_framework import FilterSet
from recipes.models import Ingredient, Recipe, Tag
from rest_framework.filters import SearchFilter


class RecipeFilter(FilterSet):
    tags = filter.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        label='Tags',
        to_field_name='slug'
    )

    class Meta:
        model = Recipe
        fields = ('tags',)


class IngredientFilter(SearchFilter):
    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ('name',)
