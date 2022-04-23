# Internal
from . import auth
from app.forms import AuthForm
from app.firestore_service import register_user, get_user
from app.models import UserData, UserModel

# Flask and extensions
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user

# Security
from werkzeug.security import generate_password_hash, check_password_hash


@auth.route(
    '/signup',
    methods=['GET', 'POST']
)
def signup():
    signup_form = AuthForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)

        if not user_doc.to_dict():
            hashed_password = generate_password_hash(password)
            user_data = UserData(username, hashed_password)
            register_user(user_data)

            user_model = UserModel(user_data)

            login_user(user_model)

            flash('Signed up successfully!')

            return redirect(url_for('hello'))

        else:
            flash('Username already exists')

    return render_template('signup.html', **context)


@auth.route(
    rule='/login',
    methods=['GET', 'POST']
)
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    login_form = AuthForm()
    context = {
        'login_form': AuthForm()
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict():
            db_password = user_doc.to_dict()['password']

            if check_password_hash(db_password, password):
                user_data = UserData(username, password)
                user_model = UserModel(user_data)

                # Hay que hacer el login con el user model para que tenga las caracteristicas que requiere flask-login
                login_user(user_model)

                flash('Welcome again!')

                return redirect(url_for('hello'))
            
            else:
                flash('Invalid password')

        else:
            flash('Username does not exist')

        return redirect(url_for('auth.login'))

    return render_template('login.html', **context)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully. Hope to see you soon!')
    return redirect(url_for('auth.login'))