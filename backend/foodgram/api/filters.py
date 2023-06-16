from django_filters import rest_framework as filter
from django_filters.rest_framework import FilterSet
from rest_framework.filters import SearchFilter
from recipes.models import Recipe, Tag, Ingredient


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
