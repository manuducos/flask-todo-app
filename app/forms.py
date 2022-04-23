from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class AuthForm(FlaskForm):
    username = StringField(
        'Username', 
        validators=[
            DataRequired(), 
            Length(min=5, max=16)
            ]
        )
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(), 
            Length(min=8, max=16)
            ]
        )
    submit = SubmitField('Send')

class ToDoForm(FlaskForm):
    description = StringField(
        'Description', 
        render_kw={"placeholder": "..."}, 
        validators=[DataRequired()]
        )
    submit = SubmitField('Create')