import json

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load data from a JSON file'

    def handle(self, *args, **options):
        filename = 'data/ingredients.json'
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                my_model = Ingredient(**item)
                my_model.save()
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
