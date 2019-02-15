from . import admin
from flask import abort, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, logout_user
from .forms import RegistrationForm, AdminRegistrationForm
from ..models import User, CargoRoutes


def check_admin():
    """
    Prevent non-admins from accessing this page
    """

    if not current_user.is_admin:
        abort(403)


@admin.route('/dashboard')
@login_required
def admin_dashboard():
    # prevent non admins from accessing route
    check_admin()
    users = User.query.all()
    return render_template('admin/admin_dashboard.html', users=users)


@admin.route('/transporters')
@login_required
def transporters():
    check_admin()
    page = request.args.get('page', 1, type=int)
    transporters = User.query.filter_by(is_transporter=True).order_by(
        User.id.desc()).paginate(page=page, per_page=5)
    return render_template('admin/transporters.html', transporters=transporters)


@admin.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    from app import db
    """
    Delete a user
    """
    check_admin()
    user = User.query.get_or_404(id)
    if user.is_admin:
        flash(f'You cannot remove an admin user', 'warning')
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash(f'You have successfully deleted a user', 'success')
    return redirect(url_for('admin.admin_dashboard'))


@admin.route('/transporter/<int:transporter_id>')
@login_required
def get_transporter(transporter_id):
    transporter = User.query.filter_by(id=transporter_id).first()
    return render_template('admin/transporter.html', title='Admin | Transporter', transporter=transporter)


@admin.route('/transporter/<int:transporter_id>/delete', methods=['POST'])
@login_required
def delete_transporter(transporter_id):
    check_admin()
    transporter = User.query.get_or_404(transporter_id)
    if not current_user.is_admin:
        abort(403)
    db.session.delete(transporter)
    db.session.commit()
    flash(f'Your transporter has been deleted', 'success')
    return redirect(url_for('admin.transporters'))


@admin.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    from app import db
    """
    Handle requests to the /register route
    Add an user to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    id_number=form.id_number.data,
                    phone_number=form.phone_number.data,
                    password=form.password.data,
                    is_transporter=form.transporter.data)
        # add user to the database
        db.session.add(user)
        db.session.commit()
        flash(f'You have successfully registered! You may now login', 'success')

        # redirect to the login page

        return redirect(url_for('admin.admin_dashboard'))
    # load registration form
    return render_template('admin/register.html', form=form, title='Registration')


@admin.route('/administrator/register', methods=['GET', 'POST'])
@login_required
def register_admin():
    from app import db
    """
    Handle requests to the /register route
    Add an user to the database through the registration form
    """
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    id_number=form.id_number.data,
                    phone_number=form.phone_number.data,
                    password=form.password.data,
                    is_admin=True)
        # add user to the database
        db.session.add(user)
        db.session.commit()
        flash(f'You have successfully registered an Administrator!', 'success')

        # redirect to the login page

        return redirect(url_for('admin.admin_dashboard'))
    # load registration form
    return render_template('admin/register.html', form=form, title='Administrator Registration')
