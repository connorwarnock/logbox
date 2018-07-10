from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import object_mapper
from sqlalchemy.sql import ClauseElement

from lib import db_session

Model = declarative_base(name='Model')
Model.query = db_session.query_property()


class CRUD:
    def save(self):
        if self.id == None:
            db_session.add(self)
        return db_session.commit()

    def destroy(self):
        db_session.delete(self)
        return db_session.commit()

    def to_s(self):
        mapper = object_mapper(self)
        items = [(p.key, getattr(self, p.key))
                 for p in [
                     mapper.get_property_by_column(c) for c in mapper.primary_key]]
        return "{0}({1})".format(
            self.__class__.__name__,
            ', '.join(['{0}={1!r}'.format(*_) for _ in items]))

    @classmethod
    def get_or_create(cls, defaults=None, **kwargs):
        instance = db_session.query(cls).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
            params.update(defaults or {})
            instance = cls(**kwargs)
            instance.save()
            return instance
