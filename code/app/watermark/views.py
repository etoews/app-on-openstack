import json
import os
import logging

from flask import render_template, current_app, request
from werkzeug.utils import secure_filename
import requests

from . import main
from .connect import get_connection

logger = logging.getLogger(__name__)


@main.route('/')
def index():
    images_url = current_app.config['API_URL'] + '/v1/images'
    headers = {'content-type': 'application/json'}
    response = requests.get(images_url, headers=headers)
    image_hrefs = [image['href'] for image in response.json()['images']]

    return render_template('index.html', image_hrefs=image_hrefs)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


def save_file_local(f, filename):
    abs_path = os.path.join(current_app.config['TMP_DIR'], filename)
    f.save(abs_path)

    logger.debug('Saved file locally: %s' % abs_path)


def save_file_remotely(filename):
    conn = get_connection(current_app.config)
    abs_path = os.path.join(current_app.config['TMP_DIR'], filename)

    with open(abs_path, 'rb') as f:
        conn.object_store.create_object(
            data=f.read(), name=filename, container=current_app.config['NAME'])

    logger.debug('Saved file remotely: {region}/{container}/{filename}'.format(
        region=current_app.config['OS_REGION_NAME'],
        container=current_app.config['NAME'],
        filename=filename
    ))


def create_image_message(filename):
    images_url = current_app.config['API_URL'] + '/v1/images'
    headers = {'content-type': 'application/json'}
    message = json.dumps({'filename': filename})
    requests.post(images_url, headers=headers, json=message)

    logger.debug("Created image messages: %s" % message)


@main.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')

    f = request.files['file']

    if allowed_file(f.filename):
        filename = secure_filename(f.filename)

        save_file_local(f, filename)
        save_file_remotely(filename)
        create_image_message(filename)

        return render_template('success.html')
    else:
        error = 'File type not allowed. Only %s are allowed.' % current_app.config['ALLOWED_EXTENSIONS']
        return render_template('error.html', error=error)
