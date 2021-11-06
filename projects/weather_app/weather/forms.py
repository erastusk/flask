from flask_wtf import FlaskForm, RecaptchaField
from flask import  request
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import phonenumbers
from weather.models import User
import requests
url = "https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&appid=YOU_OPENWEATHER_API_KEY"




class SignupForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
   

    def validate_email(self, email):        
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    recaptcha = RecaptchaField()
    submit = SubmitField('Login')
    

class ContactUsForm(FlaskForm):
    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    businessemail = StringField('BusinessEmail', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    message = TextAreaField('Please enter your message...', validators=[DataRequired()])    
    submit = SubmitField('ContactUs')

    def validate_phone(self, phone):
        if len(phone.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse("+1" + phone.data)
        except:
            raise ValidationError('Invalid phone number.')   

class CityForm(FlaskForm):
    city = StringField('City',validators=[DataRequired()])   
    submit = SubmitField('City Name')

    def validate_city(self, city):
        city = User.query.filter_by(city=city.data).first()
        if city:
            raise ValidationError('city already exists')
        