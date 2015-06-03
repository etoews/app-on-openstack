from flask import render_template, current_app
import requests


from . import main


@main.route('/')
def index():
    url = '{scheme}://{endpoint}/v1/images'.format(
        scheme=current_app.config['API_SCHEME'],
        endpoint=current_app.config['API_ENDPOINT']
    )
    headers = {'content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    image_hrefs = [image['href'] for image in response.json()['images']]

    return render_template('index.html', image_hrefs=image_hrefs)
