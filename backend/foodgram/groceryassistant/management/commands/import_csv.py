
import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from groceryassistant.models import Ingredient


class Command(BaseCommand):
    """Загрузка в базу ингредиентов из файла CSV."""

    def add_arguments(self, parser):
        parser.add_argument('filename', default='ingredients.csv',
                            nargs='?', type=str)

    def handle(self, *args, **options):
        try:
            with open(os.path.join(settings.DATA_PATH, options['filename']),
                      'r', encoding='utf-8') as f:
                data = csv.reader(f)
                for row in data:
                    name, measurement_unit = row
                    Ingredient.objects.get_or_create(
                        name=name, measurement_unit=measurement_unit
                    )
                self.stdout.write(
                    self.style.SUCCESS(settings.SUCCESS_IMPORT)
                )
        except IntegrityError:
            return settings.DUPLICATE_INGREDIENTS
        except FileNotFoundError:
            raise CommandError(settings.ERROR_FIND_FILE)
