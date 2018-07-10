from marshmallow_sqlalchemy import ModelSchema, fields


class LogSchema(ModelSchema):
    class Meta:
        fields = ('id', 'source', 'path', 'ingested')

log_schema = LogSchema()
logs_schema = LogSchema(many=True)
