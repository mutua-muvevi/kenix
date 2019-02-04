from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, DateField)
from wtforms.validators import Required
from ..models import CargoRoutes


class CargoRouteForm(FlaskForm):
    start_point = StringField('Starting Point', validators=[Required()],
                              render_kw={'placeholder': 'Nairobi, Kenya'})
    destination = StringField('Destination', validators=[Required()],
                              render_kw={'placeholder': 'Mombasa, Kenya'})
    from_date = DateField('From', validators=[Required()],
                          render_kw={'type': 'date'})
    to_date = DateField('To', validators=[Required()],
                        render_kw={'type': 'date'})
    picture = FileField('Update Profile', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')
