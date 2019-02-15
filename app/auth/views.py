import os
from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from . import auth
from .forms import (LoginForm,
                    RequestResetForm, ResetPasswordForm)
from .. import db, mail
from ..models import User
from flask_mail import Message
from werkzeug.security import generate_password_hash


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    if current_user.is_authenticated:
        if current_user.is_transporter:
            # redirect to the transporter dashboard page after login
            return redirect(url_for('transporter.dashboard'))
        else:
            # redirect to the admin dashboard
            return redirect(url_for('admin.admin_dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        # check whether user exists in the database
        # the password entered matches the password in the database

        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            #flash(f'Logged In', 'success')
            if user.is_transporter:
                # redirect to the transporter dashboard page after login
                return redirect(url_for('transporter.dashboard'))
            else:
                # redirect to the admin dashboard
                return redirect(url_for('admin.admin_dashboard'))
        flash(f'Invalid Credentials', 'danger')
    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash(f'You have been logged out', 'success')
    # redirect to the login page
    return redirect(url_for('auth.login'))


def send_reset_email(user):

    try:
        token = user.get_reset_token()
        msg = Message('Password Reset Request',
                      sender='activecodar@gmail.com',
                      recipients=[user.email])
        msg.body = f''' To reset your password visit the following link
        {url_for('auth.reset_password', token=token, _external=True)}

        If you did not make this request ignore this email
        '''
        mail.send(msg)

    except Exception as e:
        print(e)


@auth.route('/reset-password', methods=['GET', 'POST'])
def request_reset():
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        if current_user.is_transporter:
            # redirect to the transporter dashboard page after login
            return redirect(next_page) if next_page else redirect(url_for('transporter.dashboard'))
        else:
            # redirect to the admin dashboard
            return redirect(next_page) if next_page else redirect(url_for('admin.admin_dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f'Email has been sent with password reset instructions', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_request.html', form=form, title='Request Reset Password')


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        if current_user.is_transporter:
            # redirect to the transporter dashboard page after login
            return redirect(next_page) if next_page else redirect(url_for('transporter.dashboard'))
        else:
            # redirect to the admin dashboard
            return redirect(next_page) if next_page else redirect(url_for('admin.admin_dashboard'))

    user = User.verify_reset_token(token)

    if user is None:
        flash(f'Invalid token or expired token', 'warning')
        return redirect(url_for('auth.request_reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # add user to the database
        hashed_password = generate_password_hash(form.password.data)
        user.password_hash = hashed_password
        db.session.commit()
        flash(
            f'Your password has been reset successfully! You may now login', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form, title='Reset Password')
