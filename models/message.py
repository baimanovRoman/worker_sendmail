from datetime import datetime

import os
from peewee import *

from .user import User
if os.getenv("TEST", False):
    import worker_rabbitmq.integration_test_settings as settings
else:
    import settings


class Message(Model):
    user = ForeignKeyField(User, backref="messages", null=True)
    subject = TextField(null=True)
    message = TextField(null=True)
    email_to = TextField(null=True)
    email_from = TextField(null=True)
    is_send = BooleanField(default=False)
    status_msg = TextField(null=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        database = settings.db
        table_name = "messages"
