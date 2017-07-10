from django.core.management.base import BaseCommand

from posts.models import Post


class Command(BaseCommand):
    help = 'Loads article files from disk'

    def handle(self, *args, **kwargs):
        Post.get_objects()
