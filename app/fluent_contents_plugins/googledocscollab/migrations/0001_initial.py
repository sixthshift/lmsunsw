# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fluent_contents.utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('fluent_contents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleDocsCollabItem',
            fields=[
                ('contentitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('src', models.URLField(verbose_name='Page URL')),
                ('width', models.CharField(default=b'100%', help_text='Specify the size in pixels, or a percentage of the container area size.', max_length=10, verbose_name='Width', validators=[fluent_contents.utils.validators.validate_html_size])),
                ('height', models.CharField(default=b'100%', help_text='Specify the size in pixels.', max_length=10, verbose_name='Height', validators=[fluent_contents.utils.validators.validate_html_size])),
            ],
            options={
                'verbose_name': 'GoogleDocsCollabItem',
                'verbose_name_plural': 'GoogleDocsCollabItems',
            },
            bases=('fluent_contents.contentitem',),
        ),
    ]
