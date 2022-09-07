import csv

from django.core.management import BaseCommand

from app.models import Ingredient


def parse_csv(file_path):
    data = []
    with open(
        file_path, newline='', encoding='utf-8'
    ) as f:
        for line in csv.reader(f):
            data.append(line)
    return data


def import_ingredients(data):
    ingredients = [
        Ingredient(
            name=line[0],
            measurement_unit=line[1]
        ) for line in data
    ]
    Ingredient.objects.bulk_create(ingredients)


class Command(BaseCommand):
    """Менеджмент команда для импорта списка ингредиентов и не более"""

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs.get('path')
        import_ingredients(parse_csv(path))
