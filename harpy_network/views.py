from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import login_user, logout_user

from harpy_network import app, db, login_manager
from harpy_network.models.users import User
from harpy_network.models.characters import Character
from harpy_network.models.boons import Boon
from harpy_network.forms import LoginForm, AddCharacterForm, AddBoonForm

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

@app.route('/kindred')
def view_kindred():
    characters = Character.query.all()
    return render_template('kindred.html', characters=characters)

@app.route('/kindred/add', methods=['GET', 'POST'])
def add_kindred():
    form = AddCharacterForm()
    if form.validate_on_submit():
        new_kindred = Character(form.name.data)
        db.session.add(new_kindred)
        db.session.commit()
        return redirect(url_for('view_kindred'))
    else:
        render_template('add_kindred.html', form=form)
    return render_template('add_kindred.html', form=form)

@app.route('/prestation')
def view_boons():
    boons = Boon.query.filter_by(paid=False).all()
    return render_template('prestation.html', boons=boons)

@app.route('/prestation/add', methods=['GET', 'POST'])
def add_prestation():
    form = AddBoonForm()
    if request.method == "POST":
        if form.validate_on_submit():
            debtor = form.debtor.data
            creditor = form.creditor.data
            new_boon = Boon(debtor, creditor, form.boon_weight.data)
            db.session.add(new_boon)
            db.session.commit()
            return redirect(url_for('view_boons'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(field + ": "+ error, "error")
    characters = Character.query.all()
    return render_template('add_prestation.html', characters=characters, form=form)