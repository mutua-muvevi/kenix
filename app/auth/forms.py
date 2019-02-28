from flask_wtf import FlaskForm
from wtforms import (PasswordField, StringField, SubmitField,
                     BooleanField, ValidationError, SelectField)
from wtforms.validators import Required, Email, EqualTo, Length

from ..models import User


class LoginForm(FlaskForm):
    """
    Forms for logging in a user
    """
    email = StringField('Email', validators=[Required(), Email()], render_kw={
        'placeholder': 'email', 'id':'email-id'})
    password = PasswordField('Password', validators=[Required()], render_kw={
                             'placeholder': '*********'})
    remember = BooleanField('Remember Me', render_kw={'class': 'remember'})
    submit = SubmitField('Log In')


class RequestResetForm(FlaskForm):
    """
    Password reset request form
    """
    email = StringField('Email', validators=[Required(), Email()], render_kw={
        'placeholder': 'email'})
    submit = SubmitField('Request Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email.Register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[Required()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     Required(), EqualTo('password')])
    submit = SubmitField('Reset Password')
