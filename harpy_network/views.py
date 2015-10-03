from datetime import datetime

from flask import Blueprint, render_template, flash, redirect, url_for, request, abort, jsonify
from flask.ext.login import login_user, logout_user, login_required, current_user

from harpy_network import db, login_manager
from harpy_network.models.users import User
from harpy_network.models.characters import Character
from harpy_network.models.boons import Boon
from harpy_network.models.status import Status
from harpy_network.forms import LoginForm, AddCharacterForm, EditCharacterForm, AddBoonForm, EditBoonForm, \
    ChangePasswordForm, MergeCharacterForm, AddStatusForm, EditStatusForm

views = Blueprint('views', __name__, template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


@views.app_template_filter('strftime')
def _jinja2_filter_datetime(dateobj):
    return dateobj.strftime('%Y-%m-%d')


@views.route("/")
def landing_page():
    return render_template("landing_page.html")


@views.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=True)
        else:
            flash('Invalid login credentials.', "error")
            return render_template('login.html', form=form)
        flash('Logged in successfully.')
        next_url = request.args.get('next')
        print(request, request.args, next_url)
        return redirect(next_url or url_for('views.landing_page'))
    return render_template('login.html', form=form)


@views.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.landing_page'))


@views.route('/kindred')
@login_required
def view_all_kindred():
    characters = Character.query.all()
    return render_template('kindred.html', characters=characters)


@views.route('/kindred/add', methods=['GET', 'POST'])
@login_required
def add_kindred():
    form = AddCharacterForm()
    if form.validate_on_submit():
        new_kindred = Character(form.name.data)
        db.session.add(new_kindred)
        db.session.commit()
        return redirect(url_for('views.view_all_kindred'))
    else:
        render_template('add_kindred.html', form=form)
    return render_template('add_kindred.html', form=form)


@views.route('/kindred/<int:character_id>')
@login_required
def view_kindred(character_id):
    character = Character.query.filter_by(id=character_id).first()
    if not character:
        abort(404)
    return render_template('view_kindred.html', character=character)


@views.route('/kindred/<int:character_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_kindred(character_id):
    character = Character.query.filter_by(id=character_id).first()
    if not character:
        abort(404)
    form = EditCharacterForm()
    if request.method == "GET":
        form.name.data = character.name
        form.id.data = character.id
    if request.method == "POST":
        if form.validate_on_submit():
            character.name = form.name.data
            db.session.commit()
            return redirect(url_for('views.view_kindred', character_id=character.id))
    return render_template('edit_kindred.html', character=character, form=form)


@views.route('/kindred/<int:character_id>/merge', methods=['GET', 'POST'])
@login_required
def merge_kindred(character_id):
    character = Character.query.filter_by(id=character_id).first()
    if not character:
        abort(404)
    form = MergeCharacterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            merging_character = form.merging_kindred.data
            if merging_character != character:
                # This shouldn't happen as the form will not display the current character.
                character.merge_character(merging_character)
                db.session.commit()
            return redirect(url_for('views.view_kindred', character_id=character.id))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(field + ": " + error, "error")
    characters = Character.query.filter(Character.id != character.id).all()
    return render_template('merge_kindred.html', character=character, characters=characters, form=form)


@views.route('/kindred/<int:character_id>/status/<int:status_id>', methods=['GET', 'POST'])
@login_required
def view_status_for_kindred(character_id, status_id):
    status = Status.query.filter_by(id=status_id, character_id=character_id).first()
    if not status:
        abort(404)
    return render_template('view_status.html', status=status)


@views.route('/kindred/<int:character_id>/status/add', methods=['GET', 'POST'])
@login_required
def add_status_to_kindred(character_id):
    character = Character.query.filter_by(id=character_id).first()
    if not character:
        abort(404)
    form = AddStatusForm()
    if form.validate_on_submit():
        new_status = Status(character, form.name.data, form.location_earned.data, form.story.data)
        db.session.add(new_status)
        db.session.commit()
        return redirect(url_for('views.view_kindred', character_id=character_id))
    else:
        render_template('add_status.html', form=form)
    return render_template('add_status.html', form=form)


@views.route('/kindred/<int:character_id>/status/<int:status_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_status_for_kindred(character_id, status_id):
    status = Status.query.filter_by(id=status_id, character_id=character_id).first()
    if not status:
        abort(404)
    form = EditStatusForm()
    if request.method == "GET":
        form.name.data = status.name
        form.location_earned.data = status.location_earned
        form.story.data = status.story
    if request.method == "POST":
        if form.validate_on_submit():
            status.name = form.name.data
            status.location_earned = form.location_earned.data
            status.story = form.story.data
            db.session.commit()
            return redirect(url_for('views.view_status_for_kindred', character_id=character_id, status_id=status_id))
    return render_template('edit_status.html', form=form)


@views.route('/kindred/<int:character_id>/status/<int:status_id>', methods=['DELETE'])
@login_required
def delete_status_for_kindred(character_id, status_id):
    status = Status.query.filter_by(id=status_id, character_id=character_id).first()
    if not status:
        abort(404)
    db.session.delete(status)
    db.session.commit()
    response = {'message': 'Status deleted.',
            'redirect': url_for('views.view_kindred', character_id=character_id)}
    return jsonify(response)


@views.route('/prestation')
@login_required
def view_boons():
    boons = Boon.query.filter_by(paid=False).all()
    return render_template('prestation.html', boons=boons)


@views.route('/prestation/<int:boon_id>')
@login_required
def view_boon(boon_id):
    boon = Boon.query.filter_by(id=boon_id).first()
    if not boon:
        abort(404)
    return render_template('view_boon.html', boon=boon)


@views.route('/prestation/<int:boon_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_boon(boon_id):
    boon = Boon.query.filter_by(id=boon_id).first()
    if not boon:
        abort(404)
    form = EditBoonForm()
    if request.method == "POST":
        if form.validate_on_submit():
            boon.debtor = form.debtor.data
            boon.creditor = form.creditor.data
            boon.weight = form.boon_weight.data
            boon.comment = form.comment.data
            db.session.commit()
            return redirect(url_for('views.view_boon', boon_id=boon.id))
    characters = Character.query.all()
    return render_template('edit_boon.html', boon=boon, characters=characters, form=form)


@views.route('/prestation/<int:boon_id>/paid')
@login_required
def mark_boon_paid(boon_id):
    boon = Boon.query.filter_by(id=boon_id).first()
    boon.paid = True
    boon.paid_at = datetime.now()
    db.session.commit()
    if not boon:
        abort(404)
    return redirect(url_for('views.view_boon', boon_id=boon.id))


@views.route('/prestation/add', methods=['GET', 'POST'])
@login_required
def add_prestation():
    form = AddBoonForm()
    if request.method == "POST":
        if form.validate_on_submit():
            debtor = form.debtor.data
            creditor = form.creditor.data
            new_boon = Boon(debtor, creditor, form.boon_weight.data)
            new_boon.comment = form.comment.data
            db.session.add(new_boon)
            db.session.commit()
            return redirect(url_for('views.view_boons'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(field + ": "+ error, "error")
    characters = Character.query.all()
    return render_template('add_prestation.html', characters=characters, form=form)


@views.route('/profile')
@login_required
def view_profile():
    password_form = ChangePasswordForm()
    return render_template('profile.html', password_form=password_form)


@views.route('/profile/password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.session.add(current_user)
        db.session.commit()
        flash('Your password has been changed.')
        return redirect(url_for('views.view_profile'))
    else:
        return render_template('profile.html', password_form=form)

