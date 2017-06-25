from django.core.management.base import BaseCommand

from ...cache import clear_cache


class Command(BaseCommand):
    help = 'Clears the django cache'

    def handle(self, *args, **kwargs):
        clear_cache()
