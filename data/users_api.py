import flask
from flask import jsonify, request
import requests

from . import db_session
from .users import User

from werkzeug.utils import secure_filename

import os

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder="../templates"
)

@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'about', 'email', 'password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = User(
        name=request.json['name'],
        about=request.json['about'],
        email=request.json['email'],
        icon='/static/icon/standart_icon_user.svg'
    )
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/users', methods=['PUT'])
def change_users():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == request.json['name']).one_or_none()
    if user != None:
        if request.json['password']:
            if user.check_password(request.json['password']):
                user.about = request.json['about']
                user.set_password(request.json['new_password'])
                user.email = request.json['email']
                db_sess.commit()
                return jsonify({"success": "OK"})
            else:
                return jsonify({"error": "Invalid password"})
        else:
            user.about = request.json['about']
            user.email = request.json['email']
            db_sess.commit()
            return jsonify({"success": "OK"})
    else:
        return jsonify({"error": "User not found"})
    return(jsonify({"email": request.json['email'], "password": request.json['password'], "n_password": request.json['new_password'], "about": request.json['about']}))


@blueprint.route('/api/users/<int:id_user>', methods=['GET'])
def get_user_by_id(id_user):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id_user).one_or_none()
    if user != None:
        return jsonify({"name": user.name, "icon": user.icon})
    else:
        return jsonify({'error': 'Error GET'})


@blueprint.route('/api/users/<string:name_user>', methods=['GET'])
def get_users(name_user):
    if request.json:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == name_user).one_or_none()
        print(user.name)
        if user != None:
            if user.check_password(request.json["password"]):
                return jsonify({"name": user.name, "about": user.about, "email": user.email, "created_date": user.created_date, "icon": user.icon})
    return jsonify({'error': 'Error GET'})

        
    