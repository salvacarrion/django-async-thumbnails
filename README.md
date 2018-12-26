# Django Async Thumbnails
Asynchronous thumbnailing for remote storages (Google Cloud Storage, Amazon S3, Azure Storage,...)

**Django Async Thumbnails** is an extension for `sorl-thumbnail` so it can generate thumbnails in an asynchronous way.
Therefore, you only have to set this repo as its `THUMBNAIL_BACKEND`.

Install
-------

```
pip install https://github.com/salvacarrion/django-async-thumbnails.git/zipball/master
pip install -e git+git@github.com:salvacarrion/django-async-thumbnails.git
```

Setup
-------

Django Async Thumbnails needs pickle for the Celery serialization, so add this lines in `settings.py`:

```
# Celery serializer
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle']
```

> Note: In Python 3.0, the accelerated versions are considered implementation details of the pure Python versions

Then register 'asyncthumbnail', in the 'INSTALLED_APPS' section of your project's settings.

Finally, you have to set this repo as the sorl's thumbnail backend as explained above.

    THUMBNAIL_BACKEND = 'asyncthumbnail.backend.QueuedThumbnailBackend'


Typical problems
======

It's too slow with remotes storages (Google Cloud Storage, Amazon S3, Azure Storage,...)
-------------------------

This problem is usually related to how the APIs of these services work. For instance,
if you are using something like _django-storages, Apache Libcloud or similar_, the problem is that they
ask directly to the remote storage everytime you use a function such as `exists`, `url`, `size`,... 

This adds an impressive lag to our code, up to  3s/file. So if a response has 10 images (URLs) it 
would take up more than 30s.

**Fix:** To solve this problem you can create a class that inherits from the storage class so that
we can override the desired method.

```
@deconstructible
class FastStorage(Storage):
    def url(self, name):
         # your fast code (e.g: return MEDIA_URL + name)
```

Additionally, you can use caches to store metadata and only check in the DFS if there is a miss. 
(_I'd recommend using something like Redis_)


Celery doesn't detect any task
------------------------

The `create_thumbnail` method is decorated with `@shared_task` so you have to tell celery to discover all tasks.

> **See Celery documentation:** [http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)

**Still not working?** Check if you are running celery in the correct environment.
This problem is usually related to virtual environments (or similar), depending on the scope in which you are running Celery, it might detect different apps and therefore tasks.
