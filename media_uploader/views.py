import os
import datetime
from StringIO import StringIO
from media_uploader.files import ResumableFile
from media_uploader.models import Upload
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from PIL import Image
from .functions import get_storage, ensure_dir, get_chunks_subdir


def resumable(request):
    storage = get_storage()
    now = datetime.datetime.now()
    date_path = str(now.year) + '/' + str(now.month)
    if request.method == 'POST':
        chunk = request.FILES.get('file')
        r = ResumableFile(storage, request.POST)
        if r.chunk_exists:
            return HttpResponse('chunk already exists')
        r.process_chunk(chunk)
        if r.is_complete:
            basename, extension = os.path.splitext(r.filename)

            app_label = request.POST['app_label'].lower()
            object_name = request.POST['object_name'].lower()
            object_id = request.POST['object_id']

            content_type = ContentType.objects.get(app_label=app_label, model=object_name)
            u = Upload()
            #https://docs.djangoproject.com/en/1.7/ref/contrib/contenttypes/#generic-relations
            u.content_type = content_type
            u.object_id = object_id
            #content_object = GenericForeignKey('content_type', 'object_id')
            u.path = date_path
            u.original_filename = r.filename
            u.extension = extension
            u.uploader = request.user
            u.save()

            ensure_dir(get_chunks_subdir() + '/' + u.path)

            actual_filename = storage.save(u.path + '/' + r.filename, r.file)
            r.delete_chunks()
            return HttpResponse(actual_filename)
        return HttpResponse()
    elif request.method == 'GET':
        r = ResumableFile(storage, request.GET)
        if not r.chunk_exists:
            return HttpResponse('chunk not found', status=404)
        if r.is_complete:
            actual_filename = storage.save(date_path, r.filename, r.file)
            r.delete_chunks()
            return HttpResponse(actual_filename)
        return HttpResponse('chunk already exists')


def thumbnail(request, upload_id):
    try:
        upload = Upload.objects.get(pk=upload_id)
    except Upload.DoesNotExist:
        return redirect(settings.STATIC_URL + 'media_uploader/blank.gif')
    image_path = upload.get_absolute_file_path()
    if not os.path.exists(image_path):
        return redirect(settings.STATIC_URL + 'media_uploader/blank.gif')
    f = open(image_path, "rb")
    image = Image.open(f)
    width = getattr(settings, 'MEDIA_UPLOADER_THUMB_WIDTH', 100)
    height = getattr(settings, 'MEDIA_UPLOADER_THUMB_HEIGHT', 100)
    image.thumbnail((100, 100), Image.ANTIALIAS)
    if image.mode != "RGB":
        image = image.convert("RGB")
    out = StringIO()
    image.save(out, "JPEG")

    return HttpResponse(out.getvalue(), content_type='image/jpeg')

def resize(request, upload_id, width, height):
    try:
        upload = Upload.objects.get(pk=upload_id)
    except Upload.DoesNotExist:
        return HttpResponse("error")
    image_path = upload.get_absolute_file_path()
    if not os.path.exists(image_path):
        return HttpResponse("error")
    f = open(image_path, "rb")
    image = Image.open(f)
    width = int(width)
    height = int(height)
    image.thumbnail((width, height), Image.ANTIALIAS)
    if image.mode != "RGB":
        image = image.convert("RGB")
    new_image_path = image_path + "_resized_%s.jpg" % width
    new_image_url = upload.get_absolute_url() + "_resized_%s.jpg" % width
    new_f = open(new_image_path, "wb")
    image.save(new_f, "JPEG")
    new_f.close()
    f.close()
    return HttpResponse(new_image_url)

def upload_delete(request, id):
    up = Upload.objects.get(pk=id)
    os.remove(up.get_absolute_file_path())
    up.delete()
    return HttpResponse("deleted")
