# app/transporter/views.py

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
from ..models import CargoRoutes, User, Drivers, Vehicles
from . import transporter
from .forms import CargoRouteForm, UpdateForm, DriverForm, VehicleForm, DriverUpdateForm, NewPasswordForm


def check_transporter():
    """
    Prevent non cargo owners from accessing views
    """

    if not current_user.is_transporter:
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
    # pic_fn = picture filename which is a concantanation of the filename(hex name) and file extension
    pic_fn = random_hex + pic_ext
    # path to picture from the root to the profile_pics folder
    pic_path = os.path.join(app.root_path, 'static/profile_pics', pic_fn)
    output_size = (512, 512)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(pic_path)  # save the picture path to the file system
    return pic_fn

@transporter.route('/transporter/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    Render the homepage template on the / route
    """
    check_transporter()
    user = User.query.filter_by(
        id_number=current_user.id_number).first_or_404()
    page = request.args.get('page', 1, type=int)
    route_list = CargoRoutes.query.filter_by(routes=user)\
        .order_by(CargoRoutes.id.desc()).paginate(page=page, per_page=5)
    drivers = Drivers.query.filter_by(driver=user)\
        .order_by(Drivers.id.desc()).paginate(page=page, per_page=5)
    trucks = Vehicles.query.filter_by(vehicle=user)\
        .order_by(Vehicles.id.desc()).paginate(page=page, per_page=5)
    user = User.query.filter_by(
        id_number=current_user.id_number).first_or_404()
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone_number = form.phone_number.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Account information updated', 'success')
        return redirect(url_for('transporter.dashboard'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    return render_template('transporter/dashboard.html', title=user.first_name + " " + user.last_name,
                           image_file=image_file, form=form, route_list=route_list, drivers=drivers, trucks=trucks)

@transporter.route('/transporter/new-password', methods=['GET', 'POST'])
@login_required
def new_password():
    check_transporter()
    form = NewPasswordForm()
    if form.validate_on_submit():
        current_user.password=form.new_password.data
        db.session.commit()
        flash(f'Your Password has been updated', 'success')
        return redirect(url_for('transporter.dashboard'))
    return render_template('transporter/edit.html', form=form)


@transporter.route('/transporter/trip/post/new', methods=['GET', 'POST'])
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
    return render_template('transporter/edit.html', title='New Trip', form=form)


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

    return render_template('transporter/edit.html', title='Update Trip', form=form)


@transporter.route('/transporter/drivers/new', methods=['GET', 'POST'])
@login_required
def register_driver():
    """
    Render the homepage template on the / route
    """
    check_transporter()
    form = DriverForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.picture.data)
        driver = Drivers(
            first_name=form.first_name.data,
            middle_name=form.middle_name.data,
            last_name=form.last_name.data,
            id_number=form.id_number.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            license_number=form.license_number.data,
            image_file=picture_file,
            driver=current_user
        )
        db.session.add(driver)
        db.session.commit()
        flash(f'You have posted a job successfully', 'success')

        # redirect to employers dashboard

        return redirect(url_for('transporter.dashboard'))
    # load job posting form
    return render_template('transporter/edit.html', title='New Driver', form=form)


@transporter.route('/transporter/truck/new', methods=['GET', 'POST'])
@login_required
def register_truck():
    """
    Render the homepage template on the / route
    """
    check_transporter()
    form = VehicleForm()
    if form.validate_on_submit():
        vehicle = Vehicles(
            registration_number=form.registration_number.data,
            vehicle_type=form.vehicle_type.data,
            inspection_sticker=form.inspection_sticker.data,
            load_capacity=form.load_capacity.data,
            vehicle=current_user

        )
        db.session.add(vehicle)
        db.session.commit()
        flash(f'You have posted a job successfully', 'success')

        # redirect to employers dashboard

        return redirect(url_for('transporter.dashboard'))
    # load job posting form
    return render_template('transporter/edit.html', title='New Truck', form=form)


@transporter.route('/transporter/drivers', methods=['GET'])
@login_required
def drivers():
    page = request.args.get('page', 1, type=int)
    drivers = Drivers.query.filter_by(user_id=current_user.id).order_by(
        Drivers.id.desc()).paginate(page=page, per_page=5)
    return render_template('transporter/drivers.html', drivers=drivers, title="Kenix | Drivers")

@transporter.route('/transporter/trips', methods=['GET'])
@login_required
def trips():
    page = request.args.get('page', 1, type=int)
    trips = CargoRoutes.query.filter_by(user_id=current_user.id).order_by(
        CargoRoutes.id.desc()).paginate(page=page, per_page=5)
    return render_template('transporter/trips.html', trips=trips, title="Kenix | Trips")

@transporter.route('/transporter/trucks', methods=['GET'])
@login_required
def trucks():
    page = request.args.get('page', 1, type=int)
    trucks = Vehicles.query.filter_by(user_id=current_user.id).order_by(
        Vehicles.id.desc()).paginate(page=page, per_page=5)
    return render_template('transporter/trucks.html', trucks=trucks, title="Kenix | Trucks")


@transporter.route('/transporters/<int:driver_id>')
@login_required
def get_driver(driver_id):
    driver = Drivers.query.filter_by(id=driver_id).first()
    return render_template('transporter/driver.html',title="Driver", driver=driver)

@transporter.route('/transporter/jobs/<int:driver_id>/update', methods=['GET', 'POST'])
@login_required
def update_driver(driver_id):
    check_transporter()
    driver = Drivers.query.get_or_404(driver_id)
    if driver.driver != current_user:
        abort(403)
    form = DriverUpdateForm()
    if form.validate_on_submit():
        driver.first_name = form.first_name.data
        driver.middle_name = form.middle_name.data
        driver.last_name = form.last_name.data
        driver.id_number = form.id_number.data
        driver.email = form.email.data
        driver.phone_number = form.phone_number.data
        driver.license_number = form.license_number.data
        db.session.commit()
        flash(f'Your Driver has been updated', 'success')
        return redirect(url_for('transporter.drivers', driver_id=driver.id))
    elif request.method == 'GET':
        form.first_name.data = driver.first_name
        form.middle_name.data = driver.middle_name
        form.last_name.data = driver.last_name
        form.id_number.data = driver.id_number
        form.email.data = driver.email
        form.phone_number.data = driver.phone_number
        form.license_number.data = driver.license_number
    return render_template('transporter/edit.html', title='Update Driver', form=form)

@transporter.route('/transporter/drivers/<int:driver_id>/delete', methods=['POST'])
@login_required
def delete_driver(driver_id):
    check_transporter()
    driver = Drivers.query.get_or_404(driver_id)
    if driver.driver != current_user:
        abort(403)
    db.session.delete(driver)
    db.session.commit()
    flash(f'Your Driver has been deleted', 'success')
    return redirect(url_for('transporter.drivers'))

@transporter.route('/transporters/trucks/<int:truck_id>')
@login_required
def get_truck(truck_id):
    truck = Vehicles.query.filter_by(id=truck_id).first()
    return render_template('transporter/truck.html',title="Truck", truck=truck)

@transporter.route('/transporter/trucks/<int:truck_id>/update', methods=['GET', 'POST'])
@login_required
def update_truck(truck_id):
    check_transporter()
    truck = Vehicles.query.get_or_404(truck_id)
    if truck.vehicle != current_user:
        abort(403)
    form = VehicleForm()
    if form.validate_on_submit():
        truck.registration_number = form.registration_number.data
        truck.vehicle_type = form.vehicle_type.data
        truck.inspection_sticker = form.inspection_sticker.data
        truck.load_capacity = form.load_capacity.data
        db.session.commit()
        flash(f'Your Truck Details have been updated', 'success')
        return redirect(url_for('transporter.trucks', truck_id=truck.id))
    elif request.method == 'GET':
        form.registration_number.data = truck.registration_number
        form.vehicle_type.data = truck.vehicle_type
        form.inspection_sticker.data = truck.inspection_sticker
        form.load_capacity.data = truck.load_capacity
    return render_template('transporter/edit.html', title='Update Truck', form=form)

@transporter.route('/transporter/trucks/<int:truck_id>/delete', methods=['POST'])
@login_required
def delete_truck(truck_id):
    check_transporter()
    truck = Vehicles.query.get_or_404(truck_id)
    if truck.vehicle != current_user:
        abort(403)
    db.session.delete(truck)
    db.session.commit()
    flash(f'Your Truck has been deleted', 'success')
    return redirect(url_for('transporter.trucks'))

#===============================================================================

@transporter.route('/transporters/trips/<int:trip_id>')
@login_required
def get_trip(trip_id):
    trip = CargoRoutes.query.filter_by(id=trip_id).first()
    return render_template('transporter/trip.html',title="Trip", trip=trip)

@transporter.route('/transporter/trips/<int:trip_id>/update', methods=['GET', 'POST'])
@login_required
def update_trip(trip_id):
    check_transporter()
    trip = CargoRoutes.query.get_or_404(trip_id)
    if trip.routes != current_user:
        abort(403)
    form = CargoRouteForm()
    if form.validate_on_submit():
        trip.start_point = form.start_point.data
        trip.destination = form.destination.data
        trip.from_date = form.from_date.data
        trip.to_date = form.to_date.data
        db.session.commit()
        flash(f'Your Trip Details have been updated', 'success')
        return redirect(url_for('transporter.trips', trip_id=trip.id))
    elif request.method == 'GET':
        form.start_point.data = trip.start_point
        form.destination.data = trip.destination
        form.from_date.data = trip.from_date
        form.to_date.data = trip.to_date
    return render_template('transporter/edit.html', title='Update Trip', form=form)

@transporter.route('/transporter/trips/<int:trip_id>/delete', methods=['POST'])
@login_required
def delete_trip(trip_id):
    check_transporter()
    trip = CargoRoutes.query.get_or_404(trip_id)
    if trip.routes != current_user:
        abort(403)
    db.session.delete(trip)
    db.session.commit()
    flash(f'Your Trip has been deleted', 'success')
    return redirect(url_for('transporter.trips'))

#===========================================================================================

@transporter.route('/transporter/routes', methods=['GET'])
@login_required
def transporter_routes():
    page = request.args.get('page', 1, type=int)
    routes_list = CargoRoutes.query.order_by(
        CargoRoutes.id.desc()).paginate(page=page, per_page=5)
    return render_template('transporter/jobs.html', routes_list=routes_list, title="Apex | Routes")


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
