from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from application.models import CheckAdmin, BannedChars, User, Category, Product, CheckPostcode


class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30), BannedChars(), CheckAdmin(message="Name cannot be 'admin'.")])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=30)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=2, max=30), BannedChars(), Regexp('^[0-9]*$', message='Phone number must be numeric.')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=30), BannedChars()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=2, max=30), BannedChars(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists.')
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Login')

class AddressForm(FlaskForm):
    house_name_num = StringField('House Name/Number', validators=[DataRequired(), Length(min=1, max=30), BannedChars()])
    street = StringField('Street', validators=[DataRequired(), Length(min=1, max=30), BannedChars()])
    town_city = StringField('Town/City', validators=[DataRequired(), Length(min=2, max=30), BannedChars()])
    postcode = StringField('Postcode', validators=[DataRequired(), CheckPostcode(message='Invalid postcode.')])
    submit = SubmitField('Update')

class PaymentForm(FlaskForm):
    cardholder_name = StringField('Cardholder Name', validators=[DataRequired(), Length(min=2, max=30), BannedChars()])
    card_number = StringField('Card Number', validators=[DataRequired(), Length(min=16, max=16), BannedChars(), Regexp('^[0-9]*$', message='Card number must be numeric.')])
    expiry_date = StringField('Expiry Date', validators=[DataRequired(), Length(min=5, max=7), BannedChars(), Regexp('^(0[1-9]|1[0-2])\/(0[0-9]|1[0-9]|2[0-9]|3[0-9])$', message='Expiry date must be in format MM/YY.')])
    security_code = StringField('Security Code', validators=[DataRequired(), Length(min=3, max=4), BannedChars(), Regexp('^[0-9]*$', message='Security code must be numeric.')])
    submit = SubmitField('Pay')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30), BannedChars()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=30)])
    message = StringField('Message', validators=[DataRequired(), Length(min=2, max=300)])
    submit = SubmitField('Send')