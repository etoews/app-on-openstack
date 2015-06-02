from flask import current_app, jsonify, request, url_for

from ..models import Image
from . import api


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
