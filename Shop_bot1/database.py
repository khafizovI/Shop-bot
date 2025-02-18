from tortoise import Tortoise, fields
from tortoise.models import Model

class Product(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    price = fields.IntField()
    description = fields.TextField()
    photo = fields.CharField(max_length=255)

    def __str__(self):
        return self.name

class Order(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()
    product = fields.ForeignKeyField("models.Product", related_name="orders")

async def init_db():
    await Tortoise.init(
        db_url="sqlite://Shop.db",
        modules={"models": ["database"]}
    )
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()

from tortoise import fields
from tortoise.models import Model

class Orders(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()
    username = fields.CharField(max_length=255, null=True)
    order_details = fields.TextField()

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "orders"

