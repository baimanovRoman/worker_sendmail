from datetime import datetime
import os

from constants import USER_TYPE_CHOICES
from peewee import *
if os.getenv("TEST", False):
    import worker_rabbitmq.integration_test_settings as settings
else:
    import settings

class User(Model):
    email = CharField(unique=True)
    first_name = CharField(max_length=128, default="")
    last_name = CharField(max_length=128, default="")
    middle_name = CharField(max_length=128, default="")
    type = TextField(choices=USER_TYPE_CHOICES)
    email_confirmed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        database = settings.db
        table_name = "authenticate_user"
