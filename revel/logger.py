import logging

"""
Usage in other modules:

    from djangoproject.logger import log
    log.info('some output')

Note, doing this manually in other modules results in nicer output:

    import logging
    log = logging.getLogger(__name__)
    log.info('some output')

"""

# the basic logger other apps can import
log = logging.getLogger(__name__)
