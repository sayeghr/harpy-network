from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import login_user, logout_user

from harpy_network import app, login_manager
from harpy_network.models.users import User
from harpy_network.forms import LoginForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()

@app.route("/")
def landing_page():
    return render_template("landing_page.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
        else:
            flash('Invalid login credentials.', "error")
            return render_template('login.html', form=form)
        flash('Logged in successfully.')
        next_url = request.args.get('next')
        return redirect(next_url or url_for('landing_page'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('landing_page'))