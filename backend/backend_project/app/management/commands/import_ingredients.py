import csv

from django.core.management import BaseCommand

from app.models import IngredientUnit, MeasureUnit


def parse_csv(file_path):
    data = []
    with open(
        file_path, newline='', encoding='utf-8'
    ) as f:
        for line in csv.reader(f):
            data.append(line)
    return data


def import_ingridients(data):
    measure_units = set([line[1] for line in data])
    print(measure_units)
    MeasureUnit.objects.bulk_create(
        [MeasureUnit(name=unit) for unit in measure_units]
    )
    for line in data:
        obj, created = IngredientUnit.objects.get_or_create(
            name=line[0]
        )
        measurement_units = MeasureUnit.objects.filter(name=line[1])
        obj.measurement_unit.set(measurement_units)
        obj.save()
        print(f'{line[0]}; {line[1]}')


class Command(BaseCommand):
    """Менеджмент команда для импорта списка ингредиентов и не более"""

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs.get('path')
        import_ingridients(parse_csv(path))
