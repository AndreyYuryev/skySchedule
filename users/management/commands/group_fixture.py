from django.core.management import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        # group_normal = Group.objects.create()
        # Создание fixtures
        call_command('dumpdata', '--natural-foreign', '--output', 'fixtures.json')
