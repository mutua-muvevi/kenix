# app/transporter/views.py

from flask import render_template
from flask_login import login_required
from flask import render_template, abort, url_for, flash, redirect, request
from flask_login import login_required, current_user
import os

# local imports
from .. import db
from .. import create_app
from ..models import CargoRoutes, User
from ..cargo_owner.views import save_picture
from . import transporter
from .forms import CargoRouteForm, UpdateForm


def check_transporter():
    """
    Prevent non cargo owners from accessing views
    """

    if not current_user.is_transporter:
        abort(403)


@transporter.route('/transporter/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    Render the homepage template on the / route
    """
    check_transporter()
    user = User.query.filter_by(id_number=current_user.id_number).first_or_404()
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
        return redirect(url_for('transporter.dashboard'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    image_file = url_for('static',
                            filename='profile_pics/' + current_user.image_file)
    return render_template('transporter/dashboard.html', title=user.first_name + " " + user.last_name,
                             image_file=image_file, form=form, route_list=route_list)

@transporter.route('/route/post/new', methods=['GET', 'POST'])
@login_required
def post_route():
    """
    Render the homepage template on the / route
    """
    check_transporter()
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

        return redirect(url_for('transporter.dashboard'))
    # load job posting form
    return render_template('transporter/project.html', title='New Job', form=form)

@transporter.route('/transporter/<int:res_id>/route/update', methods=['GET', 'POST'])
@login_required
def update_route(res_id):
    check_transporter()
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
        return redirect(url_for('transporter.dashboard'))
    elif request.method == 'GET':
        form.start_point.data = current_user.start_point
        form.destination.data = current_user.destination
        form.from_date.data = current_user.from_date
        form.to_date.data = current_user.to_date

    return render_template('transporter/resume.html', title='Update Route', form=form)

@transporter.route('/transporters', methods=['GET', 'POST'])
@login_required
def transporters():
    page = request.args.get('page', 1, type=int)
    transporters = User.query.filter_by(is_transporter=True).order_by(
        User.id.desc()).paginate(page=page, per_page=5)
    cargo_routes = CargoRoutes.query.all()
    return render_template('transporter/transporters.html', cargo_routes=cargo_routes, transporters=transporters, title="Kenix | Transporters")

@transporter.route('/transporters/<int:transporter_id>')
@login_required
def get_transporter(transporter_id):
    user = User.query.filter_by(id=transporter_id).first()
    try:
        routes_by_id = CargoRoutes.query.filter_by(routes=user).all()
        print(routes_by_id)
        return render_template('transporter/transporter.html',
                            routes_by_id=routes_by_id, title="Transporter", user=user)
    except Exception as e:
        print(e)
        abort(404) 

@transporter.route('/transporter/route/<int:route_id>/delete', methods=['POST'])
@login_required
def delete_project(route_id):
    check_transporter()
    route = CargoRoutes.query.get_or_404(route_id)
    if route.architect != current_user:
        abort(403)
    db.session.delete(route)
    db.session.commit()
    flash(f'Your Project has been deleted', 'success')
    return redirect(url_for('transporter.dashboard'))
