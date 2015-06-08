import logging

from flask import current_app, jsonify, request, url_for
import requests
from openstack.message.v1 import message

from ..connect import get_connection
from ..models import Image, db
from . import api

requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)

@api.route('/images')
def get_images():
    page = request.args.get('page', 1, type=int)
    pagination = Image.query.paginate(
        page, per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False)
    images = pagination.items

    logger.debug("Got images: %s" % images)

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
        client=current_app.config['CLIENT'], queue=current_app.config['NAME'],
        ttl=600, body=request.json)]

    get_connection(current_app.config).message.create_messages(messages)

    logger.debug("Created image messages: %s" % messages[0])

    return '', 202

@api.route('/images', methods=['PUT'])
def update_image():
    image = Image(href='{container}/{filename}'.format(
        container=current_app.config['CONTAINER_CDN_URL'],
        filename=request.json['filename']))
    db.session.add(image)
    db.session.commit()

    logger.debug("Updated image: %s" % image)

    return '', 200
