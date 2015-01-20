from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from .functions import get_chunks_subdir
import uuid


chunks_subdir = get_chunks_subdir()

class Upload(models.Model):
    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4)
    #https://docs.djangoproject.com/en/1.7/ref/contrib/contenttypes/#generic-relations
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    uploaded = models.DateTimeField(auto_now_add=True)
    original_filename = models.CharField(max_length=255)
    extension = models.CharField(max_length=7)
    path = models.CharField(max_length=10)

    uploader = models.ForeignKey(settings.AUTH_USER_MODEL)

    def get_absolute_url(self):
        return ''.join([settings.MEDIA_URL, chunks_subdir, '/', self.path, '/', self.original_filename])

    def get_absolute_file_path(self):
        return ''.join([settings.MEDIA_ROOT, '/', chunks_subdir, '/', self.path, '/', self.original_filename])

    def is_image(self):
        return self.extension.lower() in ['.jpg', '.jpeg', '.gif', '.png']
