# app/freelancer/views.py

from flask import render_template
from flask_login import login_required
from flask import render_template, abort, url_for, flash, redirect, request
from flask_login import login_required, current_user
import os
import secrets
from PIL import Image
# local imports
from .. import db
from .. import create_app
from ..models import CargoRoutes, User
from . import cargo_owner
from .forms import CargoRouteForm, UpdateForm


def check_cargo_owner():
    """
    Prevent non cargo owners from accessing views
    """

    if not current_user.is_cargo_owner:
        abort(403)


def save_picture(form_picture):
    """
    function for saving the path to the profile picture
    """
    app = create_app(config_name=os.getenv('APP_SETTINGS'))
    # random hex to be usedin storing the file name to avoid clashes
    random_hex = secrets.token_hex(8)
    # split method for splitting the filename from the file extension
    _, pic_ext = os.path.split(form_picture.filename)
    # pic_fn = picture filename which is a concatanation of the filename(hex name) and file extension
    pic_fn = random_hex + pic_ext
    # path to picture from the root to the profile_pics folder
    pic_path = os.path.join(app.root_path, 'static/profile_pics', pic_fn)
    output_size = (512, 512)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(pic_path)  # save the picture path to the file system
    return pic_fn


@cargo_owner.route('/cargo_owner/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    Render the homepage template on the / route
    """
    check_cargo_owner()
    user = User.query.filter_by(
        id_number=current_user.id_number).first_or_404()
    route_list = CargoRoutes.query.filter_by(routes=user)\
        .order_by(CargoRoutes.id.desc())
    user = User.query.filter_by(
        id_number=current_user.id_number).first_or_404()
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Account information updated', 'success')
        return redirect(url_for('cargo_owner.dashboard'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    return render_template('cargo_owner/dashboard.html', title=user.first_name + " " + user.last_name,
                           image_file=image_file, form=form, route_list=route_list)


@cargo_owner.route('/route/post/new', methods=['GET', 'POST'])
@login_required
def post_route():
    """
    Render the homepage template on the / route
    """
    check_cargo_owner()
    form = CargoRouteForm()
    if form.validate_on_submit():
        cargo_route = CargoRoutes(
            start_point=form.start_point.data,
            destination=form.destination.data,
            from_date=form.from_date.data,
            to_date=form.to_date.data,
            routes=current_user
        )
        db.session.add(cargo_route)
        db.session.commit()
        flash(f'You have posted a job successfully', 'success')

        # redirect to employers dashboard

        return redirect(url_for('cargo_owner.dashboard'))
    # load job posting form
    return render_template('cargo_owner/project.html', title='New Job', form=form)


@cargo_owner.route('/cargo_owner/<int:res_id>/route/update', methods=['GET', 'POST'])
@login_required
def update_route(res_id):
    check_cargo_owner()
    user = User.query.filter_by(id_number=current_user.id_number).first()
    res_id = user.id
    res = CargoRoutes.query.filter_by(user_id=res_id).first()
    if res.author != current_user:
        abort(403)
    form = CargoRouteForm()
    if form.validate_on_submit():
        current_user.start_point = form.start_point.data
        current_user.destination = form.destination.data
        current_user.from_date = form.from_date.data
        current_user.to_date = form.to_date.data
        db.session.commit()
        flash(f'Your Route Info has been updated', 'success')
        return redirect(url_for('cargo_owner.dashboard'))
    elif request.method == 'GET':
        form.start_point.data = current_user.start_point
        form.destination.data = current_user.destination
        form.from_date.data = current_user.from_date
        form.to_date.data = current_user.to_date

    return render_template('cargo_owner/resume.html', title='Update Route', form=form)


@cargo_owner.route('/cargo_owner/route/<int:route_id>/delete', methods=['POST'])
@login_required
def delete_project(route_id):
    check_cargo_owner()
    route = CargoRoutes.query.get_or_404(route_id)
    if route.architect != current_user:
        abort(403)
    db.session.delete(route)
    db.session.commit()
    flash(f'Your Project has been deleted', 'success')
    return redirect(url_for('freelancer.dashboard'))
