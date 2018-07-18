import logging
from pymongo import MongoClient

from . import config
from .change_stream import ChangeStream


LOG = logging.getLogger(__name__)


def run():
    config.update()
    level = logging.DEBUG if config.DEBUG else logging.INFO
    logging.basicConfig(level=level)

    LOG.info(' Connecting to MongoDB {host}:{port}'.format(**config.MONGO))
    LOG.info(' Watching ChangeStream of {target}'.format(**config.STREAM))
    LOG.info(' Options: {options}'.format(**config.STREAM))
    LOG.info(' Pipeline: {pipeline}\n'.format(**config.STREAM))

    if config.DEBUG:
        LOG.info('**DEBUG**')
        config.dump()

    client = MongoClient(**config.MONGO)

    stream = ChangeStream(
        config.STREAM['target'],
        pipeline=config.STREAM.get('pipeline'),
        options=config.STREAM.get('options'),
        client=client
    )

    try:
        for change in stream:
            LOG.info(change)
    except KeyboardInterrupt:
        LOG.warning('Stream aborted!')
        if stream.resume_token:
            LOG.info('resume_token: %s' % stream.resume_token)
        stream.close()
