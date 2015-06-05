#!/usr/bin/env python

import os

from watermark import connect

conn = connect.get_connection()
name = "{username}-{queue}".format(
    username=os.getenv('OS_USERNAME'),
    queue=connect.QUEUE)
conn.message.create_queue(name=name)

print("{name} queue created".format(name=name))
