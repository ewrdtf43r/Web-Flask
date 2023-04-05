import flask
from flask_login import LoginManager, login_user
import sqlalchemy
from flask import Flask, render_template, url_for, redirect, request, flash
from register_form import RegisterForm, LoginForm
from data import db_session
from data.users import User
from data.cards import Card

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route('/sign_up_in', methods=['GET', 'POST'])
def sign_up_in():
    form_login = LoginForm()
    form_registr = RegisterForm()
    if form_login.validate_on_submit() and request.form['submit'] == "Вход":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form_login.username.data).first()
        db_sess.close()
        print(user)
        if not user:
            flash("Пользователь не найден", "error")
            return render_template('sign_up_in.html', title='Аутификация', form_reg=form_registr, form_log=form_login)
        elif not user.check_password(form_login.password.data):
            flash("Неправильный пароль", "error")
            return render_template('sign_up_in.html', title='Аутификация', form_reg=form_registr, form_log=form_login)
        print(f"login: {form_login.username.data, form_login.password.data}")
        print(user.check_password(form_login.password.data))
        return redirect("/main")
    if form_registr.validate_on_submit() and request.form['submit'] == "Регестрация":
        print(f"registr: {form_registr.email.data, form_registr.username.data, form_registr.password.data}")
        try:
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.name == form_registr.username.data).first():
                flash("Имя пользователя занято", "error")
                return render_template('sign_up_in.html', title='Аутификация', form_reg=form_registr, form_log=form_login)
            user = User()
            user.name = form_registr.username.data
            user.about = ""
            user.email = form_registr.email.data
            user.set_password(form_registr.password.data)
            db_sess.add(user)
            db_sess.commit()
            db_sess.close()
            return redirect("/main")
        except sqlalchemy.exc.IntegrityError:
            flash("Такой email уже зарегистрирован", "error")
            return render_template('sign_up_in.html', title='Аутификация', form_reg=form_registr, form_log=form_login)
        return redirect('/main')
    return render_template('sign_up_in.html', title='Аутификация', form_reg=form_registr, form_log=form_login)

@app.route('/')
@app.route('/main')
def main_page():
    return render_template("main.html")

def main():
    db_session.global_init("db/users_and_cards.sqlite")
    app.run(port=8080, host='127.0.0.1')

if __name__ == '__main__':
    main()