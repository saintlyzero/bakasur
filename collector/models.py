from tortoise import fields, models


class Trace(models.Model):
    id = fields.IntField(pk=True)
    trace_id = fields.CharField(max_length=50)
    from_node = fields.CharField(max_length=50, null=True)
    to_node = fields.CharField(max_length=50)
    in_time = fields.IntField(null=False)
    out_time = fields.IntField(null=True)
    is_complete = fields.BooleanField(default=False)
