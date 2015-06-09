from django.core.management.base import BaseCommand
from app.tasks import importData


class Command(BaseCommand):
    help = 'Uruchamia codzienny import danych'

    def handle(self, *args, **options):
        importData()
        self.stdout.write('Uruchomiono codzienny import danych')
