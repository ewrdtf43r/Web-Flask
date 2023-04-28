import flask
from flask import jsonify, request, url_for
import requests

from . import db_session
from .cards import Card

from werkzeug.utils import secure_filename

import os

blueprint = flask.Blueprint(
    'travels_api',
    __name__,
    template_folder="../templates"
)

@blueprint.route('/api/travels/<int:id_travel>', methods=['GET'])
def get_travels_by_id(id_travel):
    db_sess = db_session.create_session()
    travel = db_sess.query(Card).filter(Card.id == id_travel).one_or_none()
    if travel != None:
        return jsonify({"title": travel.title, "img_briefly": url_for("static", filename=f"img/{travel.imgs_src_briefly}"), "content": travel.content, "briefly_content": travel.briefly_title})
    else:
        return jsonify({'error': 'Error GET'})
