from __future__ import absolute_import, unicode_literals
from celery import shared_task, task

import logging

from sorl.thumbnail import default
from sorl.thumbnail.images import ImageFile


logger = logging.getLogger(__name__)


@shared_task
def create_thumbnail(file_, geometry_string, options, name):
    thumbnail = ImageFile(name, default.storage)

    # We have to check exists() because the Storage backend does not
    # overwrite in some implementations.
    if not thumbnail.exists():
        try:
            source = ImageFile(file_)
            source_image = default.engine.get_image(source)

            # We might as well set the size since we have the image in memory
            image_info = default.engine.get_image_info(source_image)
            options['image_info'] = image_info
            size = default.engine.get_image_size(source_image)
            source.set_size(size)

            try:
                default.backend._create_thumbnail(source_image,
                                                  geometry_string, options,
                                                  thumbnail)
                default.backend._create_alternative_resolutions(source_image,
                                                                geometry_string,
                                                                options,
                                                                thumbnail.name)
            finally:
                default.engine.cleanup(source_image)

            # Need to update both the source and the thumbnail with correct sizing
            default.kvstore.set(source)
            default.kvstore.set(thumbnail, source)
        except IOError as e:
            logger.exception(e)
