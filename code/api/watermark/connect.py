#!/usr/bin/env python

import requests

from openstack import connection
from openstack import profile
from openstack.message import message_service
from openstack.message.v1 import claim
from openstack.message.v1 import message
from openstack.message.v1 import queue

requests.packages.urllib3.disable_warnings()

def get_connection(config):
    prof = profile.Profile()
    prof.set_region(prof.ALL, config['OS_REGION_NAME'])

    service = message_service.MessageService()
    service.service_type = 'rax:queues'
    service.service_name = 'cloudQueues'

    claim.Claim.service = service
    message.Message.service = service
    queue.Queue.service = service

    return connection.Connection(
        profile=prof,
        auth_url=config['OS_AUTH_URL'],
        username=config['OS_USERNAME'],
        password=config['OS_PASSWORD'])
