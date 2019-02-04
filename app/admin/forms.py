from flask_wtf import FlaskForm
from wtforms import (PasswordField, StringField, SubmitField,
                     BooleanField, ValidationError, SelectField)
from wtforms.validators import Required, Email, EqualTo, Length

from ..models import User


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    first_name = StringField('First Name', validators=[Required()], render_kw={
                             'placeholder': 'first name'})
    last_name = StringField('Last Name', validators=[Required()], render_kw={
        'placeholder': 'last name'})
    phone_number = StringField('Phone Number', validators=[Required(), Length(
        min=2, max=15)], render_kw={'placeholder': 'username'})
    id_number = StringField('ID Number', validators=[Required(), Length(
        min=2, max=15)], render_kw={'placeholder': 'username'})
    email = StringField('Email', validators=[Required(), Email()], render_kw={
                        'placeholder': 'email'})
    transporter = BooleanField('Transporter')
    cargo_owner = BooleanField('Cargo Owner')
    password = PasswordField('Password', validators=[Required()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     Required(), EqualTo('password')])
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-warning'})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')

    def validate_id_number(self, id_number):
        user = User.query.filter_by(id_number=id_number.data).first()
        if user:
            raise ValidationError('ID number already exists')

    def validate_phone_number(self, phone_number):
        user = User.query.filter_by(phone_number=phone_number.data).first()
        if user:
            raise ValidationError('Phone Number already exists')
