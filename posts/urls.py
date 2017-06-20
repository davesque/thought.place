from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'articles/$', views.post_list, name='post_list'),
    url(r'articles/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[a-zA-Z0-9\-]+)/$', views.post_detail, name='post_detail'),
]
