from tortoise import fields, models


class Trace(models.Model):
    id = fields.IntField(pk=True)
    trace_id = fields.CharField(max_length=50)
    from_node = fields.CharField(max_length=50, null=True)
    to_node = fields.CharField(max_length=50)
    in_time = fields.IntField(null=False)
    out_time = fields.IntField(null=True)
    is_complete = fields.BooleanField(default=False)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "trace_id": self.trace_id,
            "from_node": self.from_node,
            "to_node": self.to_node,
            "in_time": self.in_time,
            "out_time": self.out_time,
            "is_complete": self.is_complete
        }


