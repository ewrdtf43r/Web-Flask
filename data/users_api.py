import flask
from flask import jsonify, request
import requests

from . import db_session
from .users import User

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
        email=request.json['email']
    )
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<string:name_user>', methods=['GET'])
def get_users(name_user):
    if request.json:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == name_user).one_or_none()
        print(user.name)
        if user != None:
            if user.check_password(request.json["password"]):
                return jsonify({"name": user.name, "about": user.about, "email": user.email, "created_date": user.created_date})
    return jsonify({'error': 'Error GET'})

        
    