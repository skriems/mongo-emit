from pymongo import MongoClient


class ChangeStream(object):
    """ A ChangeStream """

    def __init__(self, target, pipeline=None, options=None, client=None):
        self.client = client or MongoClient()

        db = target
        collection = None
        if '.' in target:
            db, collection = target.strip().split('.')

        target = getattr(self.client, db)
        if collection:
            target = getattr(target, collection)

        self.target = target
        self.pipeline = pipeline or []
        self.options = options or {}
        self.cursor = self.target.watch(self.pipeline, **self.options)
        self.resume_token = None

    def __iter__(self):
        for doc in self.cursor:
            self.resume_token = doc.get('_id')
            yield doc

    def __next__(self):
        doc = next(self.cursor)
        self.resume_token = doc.get('_id')
        return doc

    def resume(self, resume_token=None):
        """ resume the stream at a specific token """

        self.resume_token = resume_token or self.resume_token

        assert self.resume_token, 'missing resume_token'

        self.options.update(dict(resume_after=self.resume_token))

        if self.cursor:
            self.close()

        self.cursor = self.target.watch(self.pipeline, **self.options)
        yield from self.__iter__()

    def close(self):
        """ close the cursor attached to self if present """
        if self.cursor:
            self.cursor.close()
