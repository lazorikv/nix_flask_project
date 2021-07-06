from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from project import models


auth = Blueprint('auth', __name__)


# @auth.route('/login')
# def login():
#     return render_template('login.html')


@auth.route('/login', methods=['GET', 'POST'])
def login_post():

    # username = request.form.get('username')
    # password = request.form.get('password')

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data['username']
            password = data['password']
            user = models.UserModel.query.filter_by(username=username).first()

            if not user and not check_password_hash(user.password, password):
                # flash('Please check your login details and try again.')
                # return redirect(url_for('auth.login'))
                return {"error": "Please check your login details and try again."}

            login_user(user)
            return {"message": f"User - {user.username} has been login successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    # return redirect(url_for('index'))


# @auth.route('/signup')
# def signup():
#     return render_template('signup.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup_post():
    # username = request.form.get('username')
    # password = request.form.get('password')

    if request.method == 'POST':
        if request.is_json:
            data = request.json
            username = data["username"]
            password = data["password"]
            user = models.UserModel.query.filter_by(username=username).first()

            if user:
                # flash('Email address already exists.')
                # return redirect(url_for('auth.signup'))
                return {"error": 'Username already exists.'}

            new_user = models.UserModel(username=username, password=generate_password_hash(password, method='sha256'))

            models.db.session.add(new_user)
            models.db.session.commit()

    # return redirect(url_for('auth.login'))
            return {"message": f"User - {new_user.username} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # return redirect(url_for('index'))
    return {"message": f"Redirected to index"}

