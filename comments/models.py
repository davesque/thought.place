from django.db import models

from thoughtplace.cache import delete_cached_fragment


class Comment(models.Model):
    url = models.CharField(db_index=True, max_length=255)
    ip = models.CharField(max_length=255)

    name = models.CharField(help_text='Name. Leave blank for anonymous comments.', max_length=255, blank=True, null=True)
    website = models.URLField(help_text='Website. Optional.', max_length=255, blank=True, null=True)

    comment = models.TextField(
        help_text='''
Comment here.  Math supported via KaTeX.  Use "$$", "\\(", or "\\[" delimiters.  To reply to someone, refer to them by name or to their comment by number e.g. "Jane #4", "comment #11", etc.
'''[1:-1],
    )

    moderator = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return '#{0} on {1} by {2}'.format(
            self.id,
            self.url,
            self.name,
        )

    def save(self, *args, **kwargs):
        self.delete_related_cache()

        super(Comment, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.delete_related_cache()

        super(Comment, self).delete(*args, **kwargs)

    def delete_related_cache(self):
        # Delete cached sections for related post or thought
        delete_cached_fragment('obj', self.url, 'comments')

    @property
    def display_name(self):
        return 'David Sanders' if self.moderator else (self.name or 'Anonymous')

    @property
    def display_website(self):
        return None if self.moderator else self.website
