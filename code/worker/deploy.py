#!/usr/bin/env python

from watermark import connect

conn = connect.get_connection()
conn.message.create_queue(name=connect.NAME)

print("{name} queue created".format(name=connect.NAME))
