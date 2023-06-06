import json

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загружает данные json по ингредиентам в модель'

    def add_arguments(self, parser):
        parser.add_argument('ingredients_file', type=str)

    def handle(self, *args, **options):
        with open(options['ingredients_file']) as f:
            data = json.load(f)
        for ingredient in data:
            Ingredient.objects.create(**ingredient)
