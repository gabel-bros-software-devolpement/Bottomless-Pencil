from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, length, Email, EqualTo
import json

class takeInput(FlaskForm):
    school = StringField('Enter the name of a school')
    submit = SubmitField('Send schools')