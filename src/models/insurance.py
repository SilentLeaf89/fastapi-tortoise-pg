from tortoise import fields
from tortoise.models import Model


class TimestampMixin:
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class Rate(Model, TimestampMixin):
    """
    The Rate model
    """
    id = fields.UUIDField(pk=True)
    date = fields.DateField(null=False)
    cargo_type = fields.CharField(max_length=255, null=False)
    rate = fields.DecimalField(max_digits=4, decimal_places=3)

    class Meta:
        unique_together = (("date", "cargo_type"), )


class Event(Model, TimestampMixin):
    """
    The Event model, created when the request with tag=["Calculate"]
    """
    id = fields.UUIDField(pk=True)
    date = fields.DateField(null=False)
    cargo_type = fields.CharField(max_length=255, null=False)
    declared_value = fields.FloatField()
    cost = fields.FloatField()
    rate = fields.ForeignKeyField("models.Rate", related_name="histories")
