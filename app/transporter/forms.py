from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, DateField,
                     ValidationError, PasswordField)
from wtforms.validators import Required, Email, Length, EqualTo
from flask_login import current_user
from ..models import CargoRoutes, User, Drivers


class NewPasswordForm(FlaskForm):
    """
    Form for users to create new password
    """
    new_password = PasswordField('New Password', validators=[Required()])
    confirm_password = PasswordField('Confirm New Password', validators=[
                                     Required(), EqualTo('new_password')])
    submit = SubmitField('Update')


class UpdateForm(FlaskForm):
    """
    Form for users to create new account
    """
    first_name = StringField('First Name', validators=[Required()], render_kw={
                             'placeholder': 'first name'})
    last_name = StringField('Last Name', validators=[Required()], render_kw={
        'placeholder': 'last name'})
    phone_number = StringField('Phone Number', validators=[Required(), Length(
        min=2, max=15)], render_kw={'placeholder': '0711123456'})
    email = StringField('Email', validators=[Required(), Email()], render_kw={
                        'placeholder': 'email'})
    picture = FileField('Update Profile', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists')

    def validate_phone_number(self, phone_number):
        if phone_number.data != current_user.phone_number:
            user = User.query.filter_by(phone_number=phone_number.data).first()
            if user:
                raise ValidationError('Phone Number already exists')


class CargoRouteForm(FlaskForm):
    start_point = StringField('Starting Point', validators=[Required()],
                              render_kw={'placeholder': 'Nairobi, Kenya'})
    destination = StringField('Destination', validators=[Required()],
                              render_kw={'placeholder': 'Mombasa, Kenya'})
    from_date = DateField('From', validators=[Required()],
                          render_kw={'type': 'date'})
    to_date = DateField('To', validators=[Required()],
                        render_kw={'type': 'date'})
    submit = SubmitField('Submit')


class DriverForm(FlaskForm):
    first_name = StringField('First Name', validators=[
                             Required()], render_kw={'placeholder': 'John'})
    middle_name = StringField('Middle Name', validators=[
                              Required()], render_kw={'placeholder': 'Doe'})
    last_name = StringField('Other Name', validators=[
                            Required()], render_kw={'placeholder': 'Willis'})
    email = StringField('Email', validators=[Required(), Email()], render_kw={
                        'placeholder': 'email@test.com'})
    id_number = StringField('Id Number', validators=[Required()], render_kw={
                            'placeholder': '23000000'})
    phone_number = StringField('Phone Number', validators=[Required()], render_kw={
                               'placeholder': '0712123456'})
    license_number = StringField('License Number', validators=[
                                 Required()], render_kw={'placeholder': 'A0126587'})
    picture = FileField('Update Profile', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')

    # def validate_phone_number(self, phone_number):
    #     if phone_number.data != current_user.drivers[phone_number]:
    #         driver = Drivers.query.filter_by(
    #             phone_number=phone_number.data).first()
    #         if driver:
    #             raise ValidationError('Phone Number already exists')

    # def validate_id_number(self, id_number):
    #     print(current_user.drivers.id_number)
    #     if id_number.data != current_user.drivers[id_number]:
    #         driver = Drivers.query.filter_by(id_number=id_number.data).first()
    #         if driver:
    #             raise ValidationError('Id Number already exists')

    # def validate_license_number(self, license_number):
    #     if license_number.data != current_user.drivers[license_number]:
    #         driver = Drivers.query.filter_by(
    #             license_number=license_number.data).first()
    #         if driver:
    #             raise ValidationError('License Number already exists')


class DriverUpdateForm(FlaskForm):
    first_name = StringField('First Name', validators=[
                             Required()], render_kw={'placeholder': 'John'})
    middle_name = StringField('Middle Name', validators=[
                              Required()], render_kw={'placeholder': 'Doe'})
    last_name = StringField('Other Name', validators=[
                            Required()], render_kw={'placeholder': 'Willis'})
    email = StringField('Email', validators=[Required(), Email()], render_kw={
                        'placeholder': 'email@test.com'})
    id_number = StringField('Id Number', validators=[Required()], render_kw={
                            'placeholder': '23000000'})
    phone_number = StringField('Phone Number', validators=[Required()], render_kw={
                               'placeholder': '0712123456'})
    license_number = StringField('License Number', validators=[
                                 Required()], render_kw={'placeholder': 'A0126587'})
    submit = SubmitField('Update')


class VehicleForm(FlaskForm):
    registration_number = StringField('Registration Number / Trailer Number', validators=[
                                      Required()], render_kw={'placeholder': 'KCA 123G/ZE 9236'})
    vehicle_type = StringField('Vehicle Type', validators=[Required()], render_kw={
                               'placeholder': 'Prime Mover, 10 Tonne Truck..'})
    inspection_sticker = StringField('Inspection Sticker', validators=[
                                     Required()], render_kw={'placeholder': 'A023254'})
    load_capacity = StringField('Load Capacity(Tonnes)', validators=[
        Required()], render_kw={'placeholder': '10000', 'type': 'float'})
    submit = SubmitField('Submit')
