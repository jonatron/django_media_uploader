from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^resumable/$', 'media_uploader.views.resumable', name='media_uploader_resumable'),
    url(r'^thumbnail/(?P<upload_id>[\w-]+)/$', 'media_uploader.views.thumbnail', name='media_uploader_thumbnail'),
)
