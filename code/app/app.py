import os

from flask import Flask, render_template, current_app
from flask.ext.bootstrap import Bootstrap
import requests

from config import config

app = Flask(__name__)
bootstrap = Bootstrap(app)

config_name = os.getenv('CONFIG_ENV') or 'default'
app.config.from_object(config[config_name])
config[config_name].init_app(app)

@app.route('/')
def index():
    url = current_app.config['API_ENDPOINT'] + '/images'
    headers = {'content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    image_hrefs = [image['href'] for image in response.json()['images']]
    return render_template('index.html', image_hrefs=image_hrefs)

if __name__ == '__main__':
    app.run(debug=True, port=4000)
