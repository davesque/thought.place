from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('ip', 'name', 'url', 'moderator', 'deleted', 'created_at')


admin.site.register(Comment, CommentAdmin)
