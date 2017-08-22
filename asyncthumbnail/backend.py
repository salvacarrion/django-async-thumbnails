from __future__ import unicode_literals

import logging

from sorl.thumbnail.conf import settings, defaults as default_settings
from sorl.thumbnail.images import ImageFile, DummyImageFile
from sorl.thumbnail import default
from sorl.thumbnail.base import ThumbnailBackend

from .tasks import create_thumbnail

logger = logging.getLogger(__name__)


class QueuedThumbnailBackend(ThumbnailBackend):

    def get_thumbnail(self, file_, geometry_string, **options):
        """
        Returns thumbnail as an ImageFile instance for file with geometry and
        options given. First it will try to get it from the key value store,
        secondly it will create it.
        """
        logger.debug('Getting thumbnail for file [%s] at [%s]', file_,
                     geometry_string)

        if file_:
            source = ImageFile(file_)
        else:
            if settings.THUMBNAIL_DUMMY:
                return DummyImageFile(geometry_string)
            else:
                logger.error('missing file_ argument in get_thumbnail()')
                return

        # preserve image filetype
        if settings.THUMBNAIL_PRESERVE_FORMAT:
            options.setdefault('format', self._get_format(source))

        for key, value in self.default_options.items():
            options.setdefault(key, value)

        # For the future I think it is better to add options only if they
        # differ from the default settings as below. This will ensure the same
        # filenames being generated for new options at default.
        for key, attr in self.extra_options:
            value = getattr(settings, attr)
            if value != getattr(default_settings, attr):
                options.setdefault(key, value)

        name = self._get_thumbnail_filename(source, geometry_string, options)
        thumbnail = ImageFile(name, default.storage)
        cached = default.kvstore.get(thumbnail)

        if cached:
            return cached

        # Create thumbnail asynchronously
        create_thumbnail.delay(file_, geometry_string, options, name)

        # Return the original image meanwhile
        thumbnail.name = file_.name
        return thumbnail
