import flask
from flask_login import LoginManager, login_user, login_required, logout_user
from flask import Flask, render_template, url_for, redirect, request, flash, make_response, jsonify
import sqlalchemy
from register_form import RegisterForm, LoginForm
from data import db_session, users_api
from data.users import User
from data.cards import Card
import requests

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/sign_up_in")

@app.route('/sign_up_in', methods=['GET', 'POST'])
def sign_up_in():
    form_login = LoginForm()
    form_registr = RegisterForm()
    if form_login.validate_on_submit() and request.form['submit'] == "Вход":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form_login.username.data).first()
        print(user)
        if not user:
            flash("Пользователь не найден", "error")
            return render_template('sign_up_in.html', title='Аутификация', form_reg=form_registr, form_log=form_login)
        elif not user.check_password(form_login.password.data):
            flash("Неправильный пароль", "error")
            return render_template('sign_up_in.html', title='Аутификация', form_reg=form_registr, form_log=form_login)
        print(f"login: {form_login.username.data, form_login.password.data}")
        login_user(user, remember=True)
        db_sess.close()
        return redirect("/main")
    if (form_registr.validate_on_submit() and request.form['submit'] == "Регестрация"):
        print(f"registr: {form_registr.email.data, form_registr.username.data, form_registr.password.data}")
        try:
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.name == form_registr.username.data).first():
                flash("Имя пользователя занято", "error")
                return render_template('sign_up_in.html', title='Аутификация', form_reg=form_registr, form_log=form_login)
            requests.post(url="http://localhost:5000/api/users", json={"name": form_registr.username.data, "password": form_registr.password.data, "email": form_registr.email.data, "about": ""}).json()
            login_user(db_sess.query(User).filter(User.name == form_login.username.data).first(), remember=True)
            return redirect("/main")
        except requests.exceptions.JSONDecodeError:
            flash("Такой email уже зарегистрирован", "error")
            return render_template('sign_up_in.html', title='Аутификация', form_reg=form_registr, form_log=form_login)
        return redirect('/main')
    if form_registr.errors.get("email"):
        if form_registr.errors.get("email")[0] == "Неправильный email":
            flash("Неправильный email", "error")
            return render_template('sign_up_in.html', title='Аутификация', form_reg=form_registr, form_log=form_login)
    return render_template('sign_up_in.html', title='Аутификация', form_reg=form_registr, form_log=form_login)
    

@app.route('/')
@app.route('/main')
def main_page():
    return render_template("main.html")

def main():
    db_session.global_init("db/users_and_cards.sqlite")
    app.register_blueprint(users_api.blueprint)
    app.run(port=5000, host='127.0.0.1')

if __name__ == '__main__':
    main()