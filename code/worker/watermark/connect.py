#!/usr/bin/env python

import os

import requests

from openstack import connection
from openstack import profile
from openstack.message import message_service
from openstack.message.v1 import claim
from openstack.message.v1 import message
from openstack.message.v1 import queue

requests.packages.urllib3.disable_warnings()

NAME = "{username}-{queue}".format(
    username=os.getenv('OS_USERNAME'),
    queue='watermark')

def get_connection():
    prof = profile.Profile()
    prof.set_region(prof.ALL, os.getenv('OS_REGION_NAME'))

    service = message_service.MessageService()
    service.service_type = 'rax:queues'
    service.service_name = 'cloudQueues'

    claim.Claim.service = service
    message.Message.service = service
    queue.Queue.service = service

    return connection.Connection(
        profile=prof,
        auth_url=os.getenv('OS_AUTH_URL'),
        username=os.getenv('OS_USERNAME'),
        password=os.getenv('OS_PASSWORD'))
