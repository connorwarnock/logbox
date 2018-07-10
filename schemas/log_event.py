from marshmallow_sqlalchemy import ModelSchema, fields


class LogEventSchema(ModelSchema):
    class Meta:
        fields = ('id', 'log_id', 'drone_id', 'drone_generation', 'start_time', 'end_time', 'lat', 'lon', 'building_layout_map', 'duration_in_seconds')

log_event_schema = LogEventSchema()
log_events_schema = LogEventSchema(many=True)
