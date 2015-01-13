from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from ..models import Upload


register = template.Library()


@register.inclusion_tag('media_uploader/upload_js.html', takes_context=True)
def upload_js(context, obj):
    app_label = obj._meta.app_label
    object_name = obj._meta.object_name
    object_id = obj.id

    chunkSize = getattr(settings, 'ADMIN_RESUMABLE_CHUNKSIZE', "1*1024*1024")
    show_thumb = getattr(settings, 'ADMIN_RESUMABLE_SHOW_THUMB', False)
    context = {
                'chunkSize': chunkSize,
                'show_thumb': show_thumb,
                'app_label': app_label,
                'object_name': object_name,
                'object_id': object_id,
              }
    return context


@register.inclusion_tag('media_uploader/upload_buttons.html')
def upload_buttons(obj):
    pass


@register.inclusion_tag('media_uploader/recent_uploads.html', takes_context=True)
def recent_uploads(context, obj):
    app_label = obj._meta.app_label.lower()
    object_name = obj._meta.object_name.lower()
    content_type = ContentType.objects.get(app_label=app_label, model=object_name)

    uploads = Upload.objects.filter(content_type=content_type, object_id=obj.id).order_by('-uploaded')
    context = {'uploads': uploads}
    return context
