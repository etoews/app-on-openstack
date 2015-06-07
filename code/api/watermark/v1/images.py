import json
import os
import uuid

from flask import current_app, jsonify, request, url_for

from ..models import Image, db
from . import api

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
client = str(uuid.uuid4())



@api.route('/images')
def get_images():
    page = request.args.get('page', 1, type=int)
    pagination = Image.query.paginate(
        page, per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False)
    images = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_images', page=page-1, _external=True)

    next = None
    if pagination.has_next:
        next = url_for('api.get_images', page=page+1, _external=True)

    return jsonify({
        'images': [image.to_json() for image in images],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })

@api.route('/images', methods=['POST'])
def create_image():
    messages = [message.Message.new(
        client=client, queue=NAME, ttl=600, body={'href': request.values['href']})]
    get_connection().message.create_messages(messages)

    return '', 202

@api.route('/images', methods=['PUT'])
def update_image():
    image = Image(href='http://43258d3051032895473e-0d4d705ac0975ecdda8f14599c5f4b64.r80.cf5.rackcdn.com/' + request.json['href'])
    db.session.add(image)
    db.session.commit()
    return '', 200

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
