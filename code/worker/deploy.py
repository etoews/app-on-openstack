#!/usr/bin/env python

import uuid

from openstack.message.v1 import message

from watermark import connect

conn = connect.get_connection()
# conn.message.create_queue(name=connect.QUEUE)

print("%s queue created" % connect.QUEUE)

client = str(uuid.uuid4())

message1 = message.Message.new(client=client, queue=connect.QUEUE, ttl=300,
                               body={'key': 'value'})
messages = conn.message.create_messages([message1])

print("%s message created" % messages[0])
