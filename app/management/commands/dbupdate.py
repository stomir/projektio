from django.core.management.base import BaseCommand
from app.tasks import importDaily


class Command(BaseCommand):
    help = 'Uruchamia codzienny import daych'

    def handle(self, *args, **options):
        importDaily()
        self.stdout.write('Uruchomiono codzienny import daych')
