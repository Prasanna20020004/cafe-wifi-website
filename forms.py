from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, BooleanField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    map_link = URLField("Map Link", validators=[DataRequired()])
    image_link = URLField("Image Link", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    sockets = BooleanField("Has Sockets", validators=[DataRequired()])
    toilet = BooleanField("Has Toilet", validators=[DataRequired()])
    wi_fi = BooleanField("Has Wi-fi", validators=[DataRequired()])
    calls = BooleanField("Can Take Calls", validators=[DataRequired()])
    seats = StringField("Number Of Seats", validators=[DataRequired()])
    price = StringField("Coffee Price", validators=[DataRequired()])
    add = SubmitField("Add")


class UpdateForm(FlaskForm):
    price = StringField("Enter new price", validators=[DataRequired()])
    update = SubmitField("Update")


class DeleteForm(FlaskForm):
    key = StringField("Enter API KEY", validators=[DataRequired()])
    delete = SubmitField("Delete")
