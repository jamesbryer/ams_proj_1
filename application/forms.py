from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import CheckAdmin, BannedChars, User, Category, Product


class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30), BannedChars()])
    email = StringField('Email', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=30), BannedChars()])
    postcode = StringField('Postcode', validators=[DataRequired(), Length(min=2, max=30), BannedChars()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=2, max=30), BannedChars()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=30), BannedChars()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=2, max=30), BannedChars(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists.')
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=30), BannedChars()])
    submit = SubmitField('Login')