import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from lib import db
from lib.database import CRUD, Model
from lib.log_parser import LogParser
from .log_event import LogEvent


class Log(Model, CRUD):
    __tablename__ = 'logs'
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()'))
    source = db.Column(sa.String())
    path = db.Column(sa.String())
    ingested = db.Column(sa.Boolean(), server_default='0', nullable=False)

    """
    Reads log from path and saves LogEvents

    @return list of parsed LogEvent
    """
    def ingest(self):
        if self.ingested: raise Error('Log has already been ingested, reset first')
        raw_log_events = LogParser(self.path).parse()
        log_events = []
        for raw_log_event in raw_log_events:
            log_events.append(self.__save_log_event(raw_log_event))
        self.ingested = True
        self.save()
        return log_events

    def __save_log_event(self, raw_log_event):
        log_event = LogEvent(log=self, **raw_log_event)
        log_event.set_duration()
        log_event.save()
        return log_event
