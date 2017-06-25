from django.contrib import messages
from django.http import Http404
from django.views.decorators.cache import never_cache
from django.views.generic.base import TemplateView

from comments.forms import CommentForm
from comments.models import Comment
from thoughtplace.cache import ONE_YEAR_TIMEOUT
from .models import Post


class PostListView(TemplateView):
    template_name = 'posts/index.html'
    pseudo_model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(*args, **kwargs)

        objects = self.pseudo_model.get_objects().values()
        objects = filter(lambda i: i.published, objects)
        objects = sorted(objects, key=lambda i: i.published, reverse=True)

        context['objects'] = objects

        return context

post_list = PostListView.as_view()


class PostDetailView(TemplateView):
    template_name = 'posts/post.html'
    pseudo_model = Post

    def post(self, *args, **kwargs):
        return super(PostDetailView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)

        post_id = (
            self.kwargs['year'],
            self.kwargs['month'],
            self.kwargs['day'],
            self.kwargs['slug'],
        )

        try:
            obj = self.pseudo_model.get_object(post_id)
        except KeyError:
            raise Http404

        context['obj'] = obj
        context['comments'] = Comment.objects.filter(url=obj.url)

        if self.request.method == 'POST':
            form = CommentForm(self.request.POST, obj=obj, request=self.request)

            if form.is_valid():
                form.save()
                messages.success(self.request, 'Your comment has been posted.')
        else:
            form = CommentForm()

        context['form'] = form
        context['ONE_YEAR_TIMEOUT'] = ONE_YEAR_TIMEOUT

        return context

post_detail = never_cache(PostDetailView.as_view())
