from flask import render_template, current_app
import requests


from . import main


@main.route('/')
def index():
    url = current_app.config['API_ENDPOINT'] + '/v1/images'
    headers = {'content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    image_hrefs = [image['href'] for image in response.json()['images']]

    return render_template('index.html', image_hrefs=image_hrefs)
