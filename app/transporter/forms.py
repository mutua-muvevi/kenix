from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, DateField, ValidationError)
from wtforms.validators import Required, Email, Length
from flask_login import current_user
from ..models import CargoRoutes, User


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


class CargoRouteForm(FlaskForm):
    start_point = StringField('Starting Point', validators=[Required()],
                              render_kw={'placeholder': 'Nairobi, Kenya'})
    destination = StringField('Destination', validators=[Required()],
                              render_kw={'placeholder': 'Mombasa, Kenya'})
    from_date = DateField('From', validators=[Required()],
                          render_kw={'type': 'date'})
    to_date = DateField('To', validators=[Required()],
                        render_kw={'type': 'date'})
    submit = SubmitField('Post')
