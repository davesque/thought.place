import os
import re

from dateutil.parser import parse
from django.conf import settings
from django.core.urlresolvers import reverse
from pypandoc import convert
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class Post(object):
    DATE_RE = re.compile(r'^.*/(\d{4})/(\d{1,2})/(\d{1,2})/([a-zA-Z0-9\-]+)\.md$')
    OBJECTS_DIR = os.path.join(settings.BASE_DIR, 'posts', 'objects')
    DETAIL_URL = 'posts_post'

    def __init__(self, path):
        with open(path, 'r') as f:
            content = f.read()

        # Get url and identifying data from file path
        self.id = self.DATE_RE.match(path).groups()
        self.url = reverse(self.DETAIL_URL, args=self.id)

        # Parse raw post content
        parts = content.split('---\n')
        parts = filter(bool, parts)

        # Load data from frontmatter yaml
        frontmatter = load(parts[0], Loader=Loader)

        self.title = frontmatter['title']

        published = frontmatter.get('published')
        self.published = parse(published) if published else None

        # Convert post body from markdown to html
        self.body = convert(parts[1].strip(), 'html', format='markdown')

    @classmethod
    def get_objects(cls):
        if hasattr(cls, '_objects') and not settings.DEBUG:
            return cls._objects

        object_files = []
        for root, dirs, files in os.walk(cls.OBJECTS_DIR):
            for f in files:
                if f.endswith('.md'):
                    object_files.append(os.path.join(root, f))

        cls._objects = {o.id: o for o in map(cls, object_files)}

        return cls._objects

    @classmethod
    def get_object(cls, id):
        return cls.get_objects()[id]
