# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=255, serialize=False, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('original_filename', models.CharField(max_length=255)),
                ('extension', models.CharField(max_length=7)),
                ('path', models.CharField(max_length=10)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('uploader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
