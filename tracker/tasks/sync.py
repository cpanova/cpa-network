from project._celery import _celery


@_celery.task
def sync():
    return 'sync done'
