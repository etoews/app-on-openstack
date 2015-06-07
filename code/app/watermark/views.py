import hmac
from hashlib import sha1
from time import time

from flask import render_template, current_app, request
import requests


from . import main


@main.route('/')
def index():
    images_url = current_app.config['API_URL'] + '/v1/images'
    headers = {'content-type': 'application/json'}
    response = requests.get(images_url, headers=headers)
    image_hrefs = [image['href'] for image in response.json()['images']]

    return render_template('index.html', image_hrefs=image_hrefs)

@main.route('/upload')
def upload():
    formpost = {
        'path': '/v1/MossoCloudFS_5bcf396e-39dd-45ff-93a1-712b9aba90a9/everett4drg-watermark',
        'redirect': request.url + '/success',
        'max_file_size': 10000000,
        'max_file_count': 1,
        'expires': int(time() + 600),
        'temp_url_key': 'qksfd84iua4KN084oniur34aoungINUIU'
    }

    hmac_body = '{path}\n{redirect}\n{max_file_size}\n{max_file_count}\n{expires}'.format(**formpost)
    signature = hmac.new(formpost['temp_url_key'], hmac_body, sha1).hexdigest()
    formpost['signature'] = signature

    return render_template('upload.html', **formpost)

@main.route('/upload/success')
def success():
    images_url = current_app.config['API_URL'] + '/v1/images'
    return render_template('success.html', api_url=images_url)
