import os
from django.core.files.storage import get_storage_class
from django.conf import settings


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def get_chunks_subdir():
    return getattr(settings, 'MEDIA_UPLOADER_SUBDIR', 'admin_uploaded')


def get_chunks_dir():
    chunks_subdir = get_chunks_subdir()
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if not media_root:
        raise ImproperlyConfigured(
            'You must set settings.MEDIA_ROOT')
    chunks_dir = os.path.join(media_root, chunks_subdir)
    ensure_dir(chunks_dir)
    return chunks_dir


def get_storage():
    """
    Looks at the ADMIN_RESUMABLE_STORAGE setting and returns
    an instance of the storage class specified.

    Defaults to django.core.files.storage.FileSystemStorage.

    Any custom storage class used here must either be a subclass of
    django.core.files.storage.FileSystemStorage, or accept a location
    init parameter.
    """
    return get_storage_class(getattr(
        settings, 'MEDIA_UPLOADER_STORAGE',
        'django.core.files.storage.FileSystemStorage'
    ))(location=get_chunks_dir())
