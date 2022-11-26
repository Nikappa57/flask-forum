from flask_wtf import FlaskForm

from wtforms.fields import EmailField
from wtforms import (validators, BooleanField, PasswordField, StringField, 
    SubmitField, TextAreaField, SelectField)
from Site.views.Main.src.messages import Error

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[
        validators.DataRequired(Error.required), 
        validators.Email()]
    )
    password = PasswordField('Password', validators=[
        validators.DataRequired(Error.required)])
    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[
        validators.DataRequired(Error.required), 
        validators.Email()]
    )
    username = StringField('Username', validators=[
        validators.DataRequired(Error.required), 
        validators.Length(min=4, max=30, message=Error.length.format(
            name='Username', min=4, max=30))
        ]
    )
    password = PasswordField('Password', validators=[
        validators.InputRequired(Error.required), 
        validators.EqualTo('confirm', message=Error.password), 
        validators.Length(min=6, max=40, message=
            Error.length.format(name='password', min=6, max=40))]
    )
    confirm = PasswordField('Confirm Password')

    submit = SubmitField('Register')

    
class ResetPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[
        validators.DataRequired("This field is required."), 
        validators.Email()])
    submit = SubmitField('Confirm')


class ResetPassword2Form(FlaskForm):
    password = PasswordField('Password', validators=[
            validators.InputRequired("This field is required."), 
            validators.EqualTo('confirm', message="Passwords don't match"), 
            validators.Length(min=6, max=40, 
                message="The Password must contain between 6 and 40 characters")])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Confirm')

