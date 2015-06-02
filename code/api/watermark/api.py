import os

from flask import Flask, jsonify, request, url_for, current_app
from flask.ext.script import Manager, Shell
from flask.ext.sqlalchemy import SQLAlchemy

from config import config

api = Flask(__name__)
db = SQLAlchemy(api)
manager = Manager(api)

config_name = os.getenv('CONFIG_ENV') or 'default'
api.config.from_object(config[config_name])
config[config_name].init_api(api)


@api.route('/')
def index():
    return '<h1>HI</h1>'

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

def make_shell_context():
    return dict(api=api, db=db, Image=Image)

manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def create_all():
    db.create_all()

@manager.command
def drop_all():
    db.drop_all()

@manager.command
def dummy_data():
    test_image_1 = Image(href="http://i.imgur.com/fTdi7VJ.png")
    test_image_2 = Image(href="http://i.imgur.com/WHdUhXw.jpg")
    db.session.add_all([test_image_1, test_image_2])
    db.session.commit()

class Image(db.Model):

    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    href = db.Column(db.String(256), unique=True, nullable=False)

    def to_json(self):
        json = {'href': self.href}
        return json

    def __repr__(self):
        return '<Image %r>' % self.url


if __name__ == '__main__':
    manager.run()
