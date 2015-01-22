Django Media Uploader
=====================

A resuable django app that provides views, models and template tags to implement resumable HTML5 uploads. Uploads can be associated with any other model instance. Uses [resumable.js](http://www.resumablejs.com/). 

Template Tag:

    {% load media_uploader %}
    {% upload_js item %}

Add to your URLs:

    url(r'', include('media_cms_core.urls', namespace='mcc')),

Add to your INSTALLED_APPS:

    'media_uploader',

Example JS for showing recent uploads:

    $(function() {
        function refresh_recent_uploads() {
            $('#recent_uploads').load('{% url 'mcc:recently_uploaded' item.id %}', function() {
            });
        }
    
        $('#refresh_uploads').click(function() {
            refresh_recent_uploads();
        });
    
    });
