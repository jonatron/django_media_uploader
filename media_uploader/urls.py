from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^resumable/$', 'media_uploader.views.resumable', name='media_uploader_resumable'),
    url(r'^thumbnail/(?P<upload_id>[\w-]+)/$', 'media_uploader.views.thumbnail', name='media_uploader_thumbnail'),
    url(r'^resize/(?P<upload_id>[\w-]+)/(?P<width>\d+)/(?P<height>\d+)/$', 'media_uploader.views.resize', name='media_uploader_resize'),
    url(r'^upload/(?P<id>[\w-]+)/delete/$', 'media_uploader.views.upload_delete', name="media_uploader_delete"),
)
