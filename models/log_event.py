import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from lib import db
from lib.database import CRUD, Model


class LogEvent(Model, CRUD):
    __tablename__ = 'log_events'
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()"))
    log_id = db.Column(db.ForeignKey('logs.id'), nullable=False, index=True)
    log = relationship('Log', backref='log_events', foreign_keys=[log_id])
    drone_id = db.Column(sa.Integer())
    drone_generation = db.Column(sa.Integer())
    start_time = db.Column(sa.DateTime())
    end_time = db.Column(sa.DateTime())
    lat = db.Column(sa.Float(precision=10))
    lon = db.Column(sa.Float(precision=10))
    building_layout_map = db.Column(sa.String())
    duration_in_seconds = db.Column(sa.Integer())

    """
    Sets the duration based on start and end times
    """
    def set_duration(self):
        if self.start_time == None or self.end_time == None: raise Error('start_time and end_time required')
        delta = self.end_time - self.start_time
        self.duration_in_seconds = delta.seconds
