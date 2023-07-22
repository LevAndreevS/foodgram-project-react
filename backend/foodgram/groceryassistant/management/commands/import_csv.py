
import csv

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from foodgram import settings
from groceryassistant.models import Ingredient


class Command(BaseCommand):
    """Загрузка в базу ингредиентов из файла CSV."""
    def handle(self, *args, **kwargs):
        try:
            with open(
                    settings.PATH + settings.FILENAME,
                    'r', encoding='utf-8') as file:
                raise CommandError(settings.ERROR_FIND_FILE)
            reader = csv.reader(file)
            for row in reader:
                data = [
                    Ingredient(
                        name=row[0],
                        measurement_unit=row[1],
                    )
                ]
                Ingredient.objects.bulk_create(data)
        except (FileNotFoundError, IntegrityError):
            return settings.DUPLICATE_INGREDIENTS
        self.stdout.write(
            self.style.SUCCESS(
                settings.SUCCESS_IMPORT.format(settings.FILENAME)
            )
        )
