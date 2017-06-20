from compressor import filters
from django.conf import settings

import sass


class LibSassFilter(filters.FilterBase):
    def input(self, **kwargs):
        return sass.compile(
            string=self.content,
            include_paths=settings.STATICFILES_DIRS,
        )
