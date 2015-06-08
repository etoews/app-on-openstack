#!/usr/bin/env python

import requests

from openstack import connection
from openstack import profile

requests.packages.urllib3.disable_warnings()

def get_connection(config):
    prof = profile.Profile()
    prof.set_region(prof.ALL, config['OS_REGION_NAME'])

    return connection.Connection(
        profile=prof,
        auth_url=config['OS_AUTH_URL'],
        username=config['OS_USERNAME'],
        password=config['OS_PASSWORD'])
