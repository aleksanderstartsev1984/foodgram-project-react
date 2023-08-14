import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from foodgram.models import Ingredient, Tag

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'Импорт ингредиентов и тэгов.'

    def add_arguments(self, parser):
        parser.add_argument('ingredients',
                            default='ingredients.csv',
                            nargs='*',
                            type=str)
        parser.add_argument('tags',
                            default='tags.csv',
                            nargs='*',
                            type=str)

    def handle(self, *args, **options):
        try:
            import_list = []
            with open(os.path.join(DATA_ROOT, options['ingredients']), 'r',
                      encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    name = row[0]
                    unit = row[1]
                    import_list.append(Ingredient(name=name,
                                                  measurement_unit=unit))
                Ingredient.objects.bulk_create(import_list)

            import_list = []
            with open(os.path.join(DATA_ROOT, options['tags']), 'r',
                      encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    name = row[0]
                    slug = row[1]
                    color = row[2]
                    import_list.append(Tag(name=name,
                                           slug=slug,
                                           color=color))
                Tag.objects.bulk_create(import_list)

            self.stdout.write(self.style.SUCCESS('IMPORT CSV OK'))

        except Exception as error:
            self.stdout.write(self.style.ERROR(f'IMPORT CSV ERROR: {error}'))
