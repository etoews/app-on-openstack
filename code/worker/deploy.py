#!/usr/bin/env python

import os

from watermark.config import config as conf
from watermark import connect

config_name = os.getenv('WM_CONFIG_ENV') or 'default'
config = conf[config_name]()

conn = connect.get_connection(config)
conn.message.create_queue(name=config.NAME)

print("{name} queue created".format(name=config.NAME))
